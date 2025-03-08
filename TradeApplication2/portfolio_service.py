from flask import Flask, request, jsonify, render_template
import os
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

app = Flask(__name__, template_folder='templates', static_folder='static')
FlaskInstrumentor().instrument_app(app)

# Setup OpenTelemetry
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(OTLPSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

# Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8080))

# In-memory storage
portfolios = {}

@app.route('/')
def index():
    """Render the portfolio list page"""
    order_service_url = os.getenv("ORDER_SERVICE_URL", "http://localhost:5002")
    return render_template('portfolio_list.html', portfolios=portfolios, order_service_url=order_service_url)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

@app.route('/update_portfolio', methods=['POST'])
def update_portfolio():
    """Update a user's portfolio with a new order"""
    try:
        order = request.json
        app.logger.info(f"Received portfolio update: {order}")
        
        user_id = order['user_id']
        
        if user_id not in portfolios:
            portfolios[user_id] = []
            
        portfolios[user_id].append(order)
        return jsonify({"status": "portfolio updated", "user_id": user_id}), 200
        
    except Exception as e:
        app.logger.error(f"Error updating portfolio: {e}")
        return jsonify({"error": str(e)}), 400

@app.route('/portfolios', methods=['GET'])
def get_portfolios():
    """Get all portfolios"""
    return jsonify(portfolios)

@app.route('/portfolios/<user_id>', methods=['GET'])
def get_portfolio(user_id):
    """Get a user's portfolio"""
    portfolio = portfolios.get(user_id, [])
    return jsonify(portfolio)

@app.route('/portfolios/view/<user_id>')
def view_portfolio(user_id):
    app.logger.info(f"Rendering portfolio view for user: {user_id}")
    """View a user's portfolio as HTML"""
    portfolio = portfolios.get(user_id, [])
    
    # Calculate total value
    total_value = 0
    for order in portfolio:
        if 'quantity' in order and 'price' in order:
            if order['order_type'].lower() == 'buy':
                total_value += order['quantity'] * order['price']
            elif order['order_type'].lower() == 'sell':
                total_value -= order['quantity'] * order['price']
    
    return render_template('portfolio_detail.html', 
                          user_id=user_id, 
                          portfolio=portfolio, 
                          total_value=total_value,
                          order_service_url=ORDER_SERVICE_URL)

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    app.logger.info(f"Starting Portfolio Service on {HOST}:{PORT}")
    app.run(host=HOST, port=PORT)