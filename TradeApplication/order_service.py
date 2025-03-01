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
    """Render the order form page"""
    return render_template('order_form.html')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

@app.route('/orders', methods=['POST'])
def create_order():
    """Create a new order and update portfolio"""
    try:
        if request.content_type == 'application/json':
            order_data = request.json
        else:
            # Handle form submission
            order_data = {
                "user_id": request.form['user_id'],
                "symbol": request.form['symbol'],
                "order_type": request.form['order_type'],
                "quantity": int(request.form['quantity']),
                "price": float(request.form['price'])
            }
        
        # Add order to local storage
        orders.append(order_data)
        
        # Attempt to connect to portfolio service
        try:
            response = requests.post(f"{PORTFOLIO_SERVICE_URL}/update_portfolio", json=order_data, timeout=5)
            
            if request.content_type == 'application/json':
                return jsonify(response.json()), 201
            else:
                # Redirect to portfolio view
                return redirect(f"{PORTFOLIO_SERVICE_URL}/portfolios/view/{order_data['user_id']}")
                
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Error connecting to portfolio service: {e}")
            error_message = f"Could not connect to portfolio service: {e}"
            
            if request.content_type == 'application/json':
                return jsonify({"error": error_message}), 500
            else:
                return render_template('error.html', error=error_message)
            
    except Exception as e:
        app.logger.error(f"Error processing order: {e}")
        error_message = str(e)
        
        if request.content_type == 'application/json':
            return jsonify({"error": error_message}), 400
        else:
            return render_template('error.html', error=error_message)

@app.route('/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    return jsonify(orders)

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Wait for a moment to ensure other services are up
    time.sleep(2)
    app.logger.info(f"Starting Order Service on {HOST}:{PORT}")
    app.logger.info(f"Portfolio Service URL: {PORTFOLIO_SERVICE_URL}")
    app.run(host=HOST, port=PORT)