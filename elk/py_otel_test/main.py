import logging
import uvicorn
from fastapi import FastAPI
import time
import requests

from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter

# ---- Logging Setup ----
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("otel-demo")

# ---- OpenTelemetry setup ----
logger.info("Setting up OpenTelemetry...")
resource = Resource.create({
    "service.name": "fastapi-otel-demo"
})

# Trace Provider
trace.set_tracer_provider(TracerProvider(resource=resource))

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(
        OTLPSpanExporter(endpoint="http://localhost:4320/v1/traces")  # → otel-collector (HTTP)
    )
)
logger.info("OpenTelemetry configured to send to http://localhost:4320/v1/traces")

# Log Provider
log_provider = LoggerProvider(resource=resource)
log_provider.add_log_record_processor(
    BatchLogRecordProcessor(
        OTLPLogExporter(endpoint="http://localhost:4320/v1/logs")
    )
)

# Attach OTLP handler to root logger
handler = LoggingHandler(level=logging.INFO, logger_provider=log_provider)
logging.getLogger().addHandler(handler)

logger.info("OpenTelemetry logs configured to send to http://localhost:4320/v1/logs")

# ---- FastAPI ----
app = FastAPI()
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()
LoggingInstrumentor().instrument(set_logging_format=True)

@app.get("/hello")
def hello():
    logger.info("✅ /hello endpoint called")
    time.sleep(0.2)
    return {"message": "Hello from Elastic + OTEL"}

@app.get("/external")
def external():
    logger.info("🌍 /external endpoint called - triggering outgoing request")
    # This external call will now be traced thanks to RequestsInstrumentor
    r = requests.get("https://httpbin.org/delay/1")
    logger.info(f"   External request finished with status {r.status_code}")
    return {"status": r.status_code}

if __name__ == "__main__":
    print("\nStarting Server... Access at http://localhost:8081")
    print("Press CTRL+C to stop.\n")
    uvicorn.run(app, host="0.0.0.0", port=8081)
