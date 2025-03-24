FROM python:3.9

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt requirements.txt

# Install Flask with compatible dependencies
RUN pip install --no-cache-dir \
    Flask==2.0.1 \
    Werkzeug==2.0.1 \
    SQLAlchemy==1.4.23 \
    Flask-SQLAlchemy==2.5.1

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install OpenTelemetry packages
RUN pip install --no-cache-dir \
    opentelemetry-distro \
    opentelemetry-instrumentation \
    opentelemetry-exporter-otlp \
    opentelemetry-instrumentation-flask \
    opentelemetry-instrumentation-psycopg2 \
    opentelemetry-instrumentation-sqlalchemy \
    opentelemetry-instrumentation-requests \
    opentelemetry-instrumentation-logging \
    aws-xray-sdk \
    watchtower
    
# Install auto-instrumentation
RUN opentelemetry-bootstrap --action=install

# Copy application code
COPY . .

# Start application with OpenTelemetry instrumentation
CMD ["opentelemetry-instrument", "python", "app.py"]