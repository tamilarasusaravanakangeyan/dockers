using OpenTelemetry.Resources;
using OpenTelemetry.Trace;
using OpenTelemetry.Metrics;

var builder = WebApplication.CreateBuilder(args);

// ---- Configuration ----
var otelSettings = builder.Configuration.GetSection("OpenTelemetry");
var otlpEndpoint = Environment.GetEnvironmentVariable("OTEL_EXPORTER_OTLP_ENDPOINT") 
    ?? otelSettings["Endpoint"] 
    ?? "http://localhost:4320";
var serviceName = Environment.GetEnvironmentVariable("OTEL_SERVICE_NAME") 
    ?? otelSettings["ServiceName"] 
    ?? "dotnet-api";
var envName = Environment.GetEnvironmentVariable("OTEL_DEPLOYMENT_ENVIRONMENT") 
    ?? otelSettings["Environment"] 
    ?? "development";

Console.WriteLine($"\n🔧 OpenTelemetry Configuration:");
Console.WriteLine($"   Service: {serviceName}");
Console.WriteLine($"   OTLP Endpoint: {otlpEndpoint}");
Console.WriteLine($"   Environment: {envName}\n");

// ---- Services ----
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddHttpClient();

// ---- Resource ----
var resourceBuilder = ResourceBuilder.CreateDefault()
    .AddService(serviceName, serviceVersion: "1.0.0")
    .AddAttributes(new Dictionary<string, object>
    {
        { "deployment.environment", envName },
        { "host.name", Environment.MachineName },
    });

// ---- OpenTelemetry ----
builder.Services
    .AddOpenTelemetry()
    .WithTracing(tracing => tracing
        .AddAspNetCoreInstrumentation(options => options.RecordException = true)
        .AddHttpClientInstrumentation(options => options.RecordException = true)
        .SetResourceBuilder(resourceBuilder)
        .AddOtlpExporter(options => options.Endpoint = new Uri(otlpEndpoint))
    )
    .WithMetrics(metrics => metrics
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddRuntimeInstrumentation()
        .SetResourceBuilder(resourceBuilder)
        .AddOtlpExporter(options => options.Endpoint = new Uri(otlpEndpoint))
    );

// ---- Logging ----
builder.Logging.ClearProviders();
builder.Logging.AddConsole();
builder.Logging.SetMinimumLevel(LogLevel.Information);

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}
else
{
    app.UseHttpsRedirection();
}
app.UseAuthorization();
app.MapControllers();

// ---- Endpoints ----
app.MapGet("/health", (ILogger<Program> logger) =>
{
    logger.LogInformation("Health check endpoint");
    return Results.Ok(new { status = "healthy", service = serviceName });
})
.WithName("Health");

app.MapGet("/api/hello/{name}", (string name, ILogger<Program> logger) =>
{
    logger.LogInformation("Hello endpoint called with name: {name}", name);
    return Results.Ok(new { message = $"Hello {name}!", service = serviceName });
})
.WithName("SayHello");

app.MapGet("/api/external", async (HttpClient httpClient, ILogger<Program> logger) =>
{
    logger.LogInformation("External API call initiated");
    try
    {
        var response = await httpClient.GetAsync("https://httpbin.org/delay/1");
        logger.LogInformation("External response: {statusCode}", response.StatusCode);
        return Results.Ok(new { external_status = response.StatusCode.ToString() });
    }
    catch (Exception ex)
    {
        logger.LogError(ex, "External API call failed");
        return Results.StatusCode(500);
    }
})
.WithName("CallExternal");

Console.WriteLine("✅ Starting Server...");
Console.WriteLine("   📊 Swagger:  https://localhost:7124/swagger/index.html");
Console.WriteLine("   🏥 Health:   https://localhost:7124/health");
Console.WriteLine("   💬 Hello:    https://localhost:7124/api/hello/World");
Console.WriteLine("   🌐 External: https://localhost:7124/api/external");
Console.WriteLine("   📡 OTEL:     " + otlpEndpoint + "\n");

app.Run();
