# .NET 8 API + OpenTelemetry → Elastic Stack

This is a minimal ASP.NET Core 8 Web API configured to send **traces**, **metrics**, and **logs** to your ELK stack via OpenTelemetry.

## Quick Start

### 1. Prerequisites
- .NET 8 SDK installed
- ELK stack running (docker-compose up -d from parent directory)

### 2. Restore & Run
```bash
dotnet restore
dotnet run --launch-profile https
```

Server will start at `https://localhost:7124`

### 3. Test Endpoints
```bash
# Health check
curl https://localhost:7124/health

# Say hello (traced)
curl https://localhost:7124/api/hello/World

# External call (traced HTTP client)
curl https://localhost:7124/api/external
```

### 4. View in Kibana
1. Open http://localhost:5601
2. Navigate to **Observability → APM**
3. You should see **dotnet-api** service
4. Click to see:
   - **Transactions** (HTTP requests)
   - **Dependencies** (outgoing HTTP calls)
   - **Logs** (application logs)
   - **Metrics** (CPU, memory, request rates)

## Configuration

### appsettings.json
Local development settings pointing to `localhost:4320` (otel-collector on host).

### appsettings.Production.json
Container settings pointing to `http://apm-server:8200` (internal Docker network).

### Environment Variables (override appsettings.json)
```bash
OTEL_SERVICE_NAME=my-api
OTEL_DEPLOYMENT_ENVIRONMENT=staging
OTEL_EXPORTER_OTLP_ENDPOINT=http://custom-collector:4320
```

## What Gets Traced?

| Component | What | How |
| --- | --- | --- |
| **HTTP Server** | Incoming requests, response times, status codes | `AddAspNetCoreInstrumentation()` |
| **HTTP Client** | Outgoing calls (external APIs, microservices) | `AddHttpClientInstrumentation()` |
| **SQL Server** | Database queries, execution time | `AddSqlClientInstrumentation()` |
| **Logs** | All .NET logging (ILogger) | `AddOpenTelemetry()` |
| **Metrics** | Request count, latency, errors, CPU, memory | `AddRuntimeInstrumentation()` |

## Data Flow

```
.NET API (Program.cs)
    ↓
OpenTelemetry SDK (in-process)
    ↓
OTLP Exporter (HttpProtobuf or gRPC)
    ↓
http://otel-collector:4320 (on host) or http://apm-server:8200 (in Docker)
    ↓
APM Server (inside elastc-agent container)
    ↓
Elasticsearch
    ↓
Kibana UI
```

## Protocols Supported

### HTTP Protobuf (default, simpler)
- Endpoint: `http://localhost:4320`
- Protocol env: `http/protobuf`
- Payload: Binary (faster, smaller)

### gRPC (alternative, lower latency)
- Endpoint: `http://localhost:4319`
- Protocol env: `grpc`
- Payload: Binary (very fast)

## Running in Docker

Create a Dockerfile:
```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /app
COPY . .
RUN dotnet publish -c Release -o out

FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app/out .
ENV ASPNETCORE_URLS=http://+:5000
ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://apm-server:8200
EXPOSE 5000
ENTRYPOINT ["dotnet", "dotnet-api.dll"]
```

Add to docker-compose.yml:
```yaml
dotnet-api:
  build: ./dotnet-example
  container_name: dotnet-api
  depends_on:
    apm-server:
      condition: service_started
  environment:
    - OTEL_EXPORTER_OTLP_ENDPOINT=http://apm-server:8200
    - OTEL_SERVICE_NAME=dotnet-api
  ports:
    - "5000:5000"
  restart: always
```

## Troubleshooting

### No traces appearing in Kibana?

1. Check service name
   ```bash
   dotnet run
   ```
   Look for `Service: dotnet-api` in console output

2. Verify OTLP endpoint is reachable
   ```bash
   curl http://localhost:4320
   ```
   Should NOT return "connection refused"

3. Check logs
   ```bash
   dotnet run --loglevel=Debug
   ```

4. Verify otel-collector is running
   ```bash
   docker logs otel-collector
   ```
   Look for "listening on 0.0.0.0:4317" and "0.0.0.0:4318"

5. Check apm-server logs
   ```bash
   docker logs apm-server
   ```

## Advanced: Custom Attributes

Add custom tags to all spans:

```csharp
builder.Services.AddOpenTelemetry()
    .WithTracing(tracing => tracing
        .SetResourceBuilder(
            OpenTelemetry.Resources.ResourceBuilder.CreateDefault()
                .AddService(serviceName)
                .AddAttributes(new Dictionary<string, object>
                {
                    { "deployment.environment", environment },
                    { "host.name", Environment.MachineName },
                    { "team", "backend" },
                    { "version", "1.0.0" },
                })
        )
    );
```

These will appear as searchable fields in Kibana.

## References

- [OpenTelemetry .NET Docs](https://opentelemetry.io/docs/instrumentation/net/)
- [OTLP Exporter](https://github.com/open-telemetry/opentelemetry-dotnet/tree/main/src/OpenTelemetry.Exporter.OpenTelemetryProtocol)
- [Elastic APM for .NET](https://www.elastic.co/en/observability/apm)
