# Langflow with Langfuse Integration

This Docker Compose setup runs Langflow with PostgreSQL database and integrates with Langfuse for observability and tracing.

## Services

- **Langflow** - AI workflow builder (Port 7860)
- **PostgreSQL** - Database for Langflow (Port 5434)

## Prerequisites

- Docker and Docker Compose installed
- Langfuse running on `http://localhost:3000` (from the ../langfuse setup)

## Quick Start

```bash
# Start all services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f langflow

# Stop all services
docker compose down
```

## Access Points

- **Langflow UI**: http://localhost:7860
- **PostgreSQL**: localhost:5434 (user: langflow, password: langflow)

## Default Credentials

- **Username**: admin
- **Password**: admin123

## Langfuse Integration

The following environment variables are configured for Langfuse integration:

```env
LANGFUSE_SECRET_KEY=sk-lf-87ae8f58-4ea7-47b3-9f38-9be6938b27bc
LANGFUSE_PUBLIC_KEY=pk-lf-4943ac35-1532-477d-968a-2dafcbac229a
LANGFUSE_HOST=http://host.docker.internal:3000
```

### How It Works

1. Langflow connects to Langfuse running on your host machine via `host.docker.internal`
2. All workflow executions are automatically traced in Langfuse
3. View traces, metrics, and analytics in the Langfuse dashboard at http://localhost:3000

## Configuration

### Change Admin Password

Edit the `docker-compose.yml` file:

```yaml
LANGFLOW_SUPERUSER_PASSWORD: your-new-password
```

Then restart:

```bash
docker compose down
docker compose up -d
```

### Update Langfuse Keys

If you need to update the Langfuse keys, edit the following in `docker-compose.yml`:

```yaml
LANGFUSE_SECRET_KEY: your-secret-key
LANGFUSE_PUBLIC_KEY: your-public-key
```

## Volumes

- `postgres_data` - PostgreSQL database files
- `langflow_data` - Langflow configuration and flows

## Troubleshooting

### Langflow can't connect to Langfuse

1. Ensure Langfuse is running: `docker compose ps` in the langfuse directory
2. Check if Langfuse is accessible: Open http://localhost:3000 in your browser
3. Verify the Langfuse keys are correct in the docker-compose.yml

### View Langflow logs

```bash
docker compose logs langflow --tail 100
```

### Reset everything

```bash
# Stop and remove containers and volumes
docker compose down -v

# Start fresh
docker compose up -d
```

## Network Architecture

```
┌─────────────────────────────────────────────────┐
│  Host Machine                                   │
│                                                 │
│  ┌──────────────┐         ┌──────────────┐    │
│  │  Langfuse    │◄────────┤  Langflow    │    │
│  │  :3000       │  traces │  :7860       │    │
│  └──────────────┘         └──────┬───────┘    │
│                                   │             │
│                           ┌───────▼───────┐    │
│                           │  PostgreSQL   │    │
│                           │  :5434        │    │
│                           └───────────────┘    │
└─────────────────────────────────────────────────┘
```

## Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `LANGFLOW_DATABASE_URL` | PostgreSQL connection string | postgresql://langflow:langflow@postgres:5432/langflow |
| `LANGFUSE_SECRET_KEY` | Langfuse secret key for authentication | (provided) |
| `LANGFUSE_PUBLIC_KEY` | Langfuse public key | (provided) |
| `LANGFUSE_HOST` | Langfuse server URL | http://host.docker.internal:3000 |
| `LANGFLOW_SUPERUSER` | Admin username | admin |
| `LANGFLOW_SUPERUSER_PASSWORD` | Admin password | admin123 |
| `LANGFLOW_SECRET_KEY` | Langflow secret key | langflow-secret-key-change-me |
| `LANGFLOW_LOG_LEVEL` | Log level | INFO |

## Production Considerations

For production use, you should:

1. **Change all default passwords and secrets**
2. **Use environment variables or .env file** for sensitive data
3. **Enable SSL/TLS** for database connections
4. **Set up proper backup** for PostgreSQL volumes
5. **Use a reverse proxy** (nginx/traefik) with SSL
6. **Implement proper authentication** and access controls

## Support

For issues related to:
- **Langflow**: https://github.com/logspace-ai/langflow
- **Langfuse**: https://github.com/langfuse/langfuse
