#!/usr/bin/env bash


export OTEL_SERVICE_NAME=pizza-app

export OTEL_TRACES_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_METRICS_EXPORTER=otlp

export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
export OTEL_PYTHON_LOG_CORRELATION=true
export OTEL_PYTHON_LOG_LEVEL=info

# Enable gzip compression.
export OTEL_EXPORTER_OTLP_COMPRESSION=gzip
# Prefer delta temporality.
export OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE=DELTA

# Uptrace Login
export OTEL_EXPORTER_OTLP_HEADERS="uptrace-dsn=http://SomeRandomToken@localhost:14318?grpc=14317"

# Export endpoint, local Uptrace instance
export OTEL_EXPORTER_OTLP_ENDPOINT=127.0.0.1:14317
export OTEL_EXPORTER_OTLP_INSECURE=true

.venv/bin/opentelemetry-instrument uvicorn main:app --port 8000