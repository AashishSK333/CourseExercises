from flask import Flask, request, jsonify, render_template, redirect, url_for
import requests
import os
import time
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

app = Flask(__name__, template_folder='templates', static_folder='static')
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

# Setup OpenTelemetry
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(OTLPSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

# Configuration
PORTFOLIO_SERVICE_URL = os.getenv("PORTFOLIO_SERVICE_URL", "http://localhost:5001")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8080))

orders = []

@app.route('/')
def index():
    """Render the SPA"""
    portfolio_service_url = os.getenv("PORTFOLIO_SERVICE_URL", "http://localhost:5001")
    # For browser use, we need external URLs
    external_portfolio_service_url = os.getenv("PORTFOLIO_SERVICE_EXTERNAL_URL", portfolio_service_url)
    return render_template('index.html', 
                          order_service_url=os.getenv("ORDER_SERVICE_EXTERNAL_URL", ""),
                          portfolio_service_url=external_portfolio_service_url)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

@app.route('/orders', methods=['POST'])
def create_order():
    """Create a new order and update portfolio API"""
    try:
        order_data = request.json
        app.logger.info(f"Received order: {order_data}")
        
        # Add order to local storage
        orders.append(order_data)
        
        # Attempt to connect to portfolio service
        try:
            response = requests.post(f"{PORTFOLIO_SERVICE_URL}/update_portfolio", json=order_data, timeout=5)
            return jsonify(response.json()), 201
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Error connecting to portfolio service: {e}")
            return jsonify({"error": f"Could not connect to portfolio service: {e}"}), 500
            
    except Exception as e:
        app.logger.error(f"Error processing order: {e}")
        return jsonify({"error": str(e)}), 400

@app.route('/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    return jsonify(orders)

if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Wait for a moment to ensure other services are up
    time.sleep(2)
    app.logger.info(f"Starting Order Service on {HOST}:{PORT}")
    app.logger.info(f"Portfolio Service URL: {PORTFOLIO_SERVICE_URL}")
    app.run(host=HOST, port=PORT)