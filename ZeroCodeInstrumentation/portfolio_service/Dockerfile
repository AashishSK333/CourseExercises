FROM python:3.9
WORKDIR /app

# Install dependencies including AWS X-Ray and CloudWatch
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install psycopg2 \
    aws-xray-sdk \
    watchtower \
    opentelemetry-distro \
    opentelemetry-instrumentation-flask \
    opentelemetry-instrumentation-psycopg2 \
    opentelemetry-instrumentation-sqlalchemy \
    opentelemetry-exporter-otlp-proto-grpc \
    opentelemetry-exporter-otlp-proto-http

# Use OpenTelemetry auto-instrumentation
RUN opentelemetry-bootstrap --action=install

COPY . .

# Wrap the application with OpenTelemetry instrumentation
CMD ["opentelemetry-instrument", "python", "app.py"]