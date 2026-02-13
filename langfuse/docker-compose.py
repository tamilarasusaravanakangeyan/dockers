services:
  postgres:
    image: postgres:15
    container_name: langfuse-postgres
    restart: always
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U langfuse"]
      interval: 3s
      timeout: 3s
      retries: 10
    environment:
      POSTGRES_USER: langfuse
      POSTGRES_PASSWORD: langfuse
      POSTGRES_DB: langfuse
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5433:5432"

  clickhouse:
    image: clickhouse/clickhouse-server:latest
    container_name: langfuse-clickhouse
    restart: always
    environment:
      CLICKHOUSE_DB: default
      CLICKHOUSE_USER: clickhouse
      CLICKHOUSE_PASSWORD: clickhouse
    volumes:
      - clickhouse_data:/var/lib/clickhouse
      - clickhouse_logs:/var/log/clickhouse-server
    ports:
      - "8123:8123"
      - "9000:9000"
    healthcheck:
      test: wget --no-verbose --tries=1 --spider http://localhost:8123/ping || exit 1
      interval: 5s
      timeout: 5s
      retries: 10
      start_period: 1s

  redis:
    image: redis:7
    container_name: langfuse-redis
    restart: always
    command: >
      --requirepass myredissecret
      --maxmemory-policy noeviction
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 3s
      timeout: 10s
      retries: 10

  minio:
    image: minio/minio:latest
    container_name: langfuse-minio
    restart: always
    entrypoint: sh
    command: -c 'mkdir -p /data/langfuse && minio server --address ":9000" --console-address ":9001" /data'
    environment:
      MINIO_ROOT_USER: minio
      MINIO_ROOT_PASSWORD: miniosecret
    ports:
      - "9090:9000"
      - "9091:9001"
    volumes:
      - minio_data:/data
    healthcheck:
      test: ["CMD", "mc", "ready", "local"]
      interval: 5s
      timeout: 5s
      retries: 5
      start_period: 1s

  langfuse:
    image: ghcr.io/langfuse/langfuse:latest
    container_name: langfuse
    depends_on:
      postgres:
        condition: service_healthy
      clickhouse:
        condition: service_healthy
      redis:
        condition: service_healthy
      minio:
        condition: service_healthy
    restart: always
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgres://langfuse:langfuse@postgres:5432/langfuse
      CLICKHOUSE_URL: http://clickhouse:8123
      CLICKHOUSE_MIGRATION_URL: clickhouse://clickhouse:9000
      CLICKHOUSE_USER: clickhouse
      CLICKHOUSE_PASSWORD: clickhouse
      CLICKHOUSE_CLUSTER_ENABLED: "false"
      NEXTAUTH_SECRET: super-secret-change-me
      NEXTAUTH_URL: http://localhost:3000
      SALT: another-secret-change-me
      ENCRYPTION_KEY: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
      TELEMETRY_ENABLED: "false"
      # Redis configuration
      REDIS_HOST: redis
      REDIS_PORT: "6379"
      REDIS_AUTH: myredissecret
      # S3/MinIO configuration
      LANGFUSE_S3_EVENT_UPLOAD_BUCKET: langfuse
      LANGFUSE_S3_EVENT_UPLOAD_REGION: auto
      LANGFUSE_S3_EVENT_UPLOAD_ACCESS_KEY_ID: minio
      LANGFUSE_S3_EVENT_UPLOAD_SECRET_ACCESS_KEY: miniosecret
      LANGFUSE_S3_EVENT_UPLOAD_ENDPOINT: http://minio:9000
      LANGFUSE_S3_EVENT_UPLOAD_FORCE_PATH_STYLE: "true"
      LANGFUSE_S3_EVENT_UPLOAD_PREFIX: events/
      LANGFUSE_S3_MEDIA_UPLOAD_BUCKET: langfuse
      LANGFUSE_S3_MEDIA_UPLOAD_REGION: auto
      LANGFUSE_S3_MEDIA_UPLOAD_ACCESS_KEY_ID: minio
      LANGFUSE_S3_MEDIA_UPLOAD_SECRET_ACCESS_KEY: miniosecret
      LANGFUSE_S3_MEDIA_UPLOAD_ENDPOINT: http://localhost:9090
      LANGFUSE_S3_MEDIA_UPLOAD_FORCE_PATH_STYLE: "true"
      LANGFUSE_S3_MEDIA_UPLOAD_PREFIX: media/

volumes:
  postgres_data:
  clickhouse_data:
  clickhouse_logs:
  minio_data:
