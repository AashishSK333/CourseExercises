import os
import logging
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_cors import CORS
from models import Trade, db
from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# Initialize X-Ray with proper daemon address
xray_recorder.configure(
    service='portfolio-service',
    daemon_address='xray-daemon:2000',
    context_missing='LOG_ERROR',
    sampling=True
)
patch_all()  # Patch all supported libraries for X-Ray tracing

# Initialize Flask app
app = Flask(__name__)

# Set up basic logging instead of CloudWatch
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
app.logger.setLevel(logging.INFO)
app.logger.info("Portfolio service starting up")

# Apply X-Ray middleware to your Flask app
XRayMiddleware(app, xray_recorder)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db/trades'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)
CORS(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/portfolio/<int:trader_id>', methods=['GET'])
def get_portfolio(trader_id):
    # Create a segment for this request
    segment = xray_recorder.begin_segment('portfolio-handler')
    subsegment = xray_recorder.begin_subsegment('calculate-portfolio')
    
    try:
        # Add annotation for filtering in X-Ray
        xray_recorder.put_annotation('trader_id', trader_id)
        
        app.logger.info(f"Portfolio requested for trader_id: {trader_id}")
        
        # Query all trades for this trader from the database
        trades = Trade.query.filter_by(trader_id=trader_id).all()
        app.logger.info(f"Found {len(trades)} trades")
        
        # Process trades to calculate portfolio positions
        positions = {}
        total_value = 0.0
        
        for trade in trades:
            symbol = trade.asset_name
            
            if symbol not in positions:
                positions[symbol] = {
                    "symbol": symbol,
                    "quantity": 0,
                    "total_cost": 0.0
                }
            
            # Update position with this trade
            trade_quantity = float(trade.quantity)
            trade_price = float(trade.price)
            
            positions[symbol]["quantity"] += trade_quantity
            positions[symbol]["total_cost"] += trade_quantity * trade_price
            
            # Update total portfolio value
            total_value += trade_quantity * trade_price
        
        # Calculate average price for each position
        position_list = []
        
        for symbol, position in positions.items():
            if position["quantity"] > 0:
                position["average_price"] = position["total_cost"] / position["quantity"]
            else:
                position["average_price"] = 0
                
            # Remove calculation field
            del position["total_cost"]
            position_list.append(position)
        
        app.logger.info(f"Calculated positions: {position_list}")
        app.logger.info(f"Total value: {total_value}")
        
        # Return portfolio data
        response = jsonify({
            "trader_id": trader_id,
            "positions": position_list,
            "total_value": total_value
        })
        
        return response
        
    except Exception as e:
        app.logger.error(f"Error calculating portfolio: {str(e)}")
        xray_recorder.add_exception(e)
        return jsonify({"error": str(e)}), 500
    finally:
        xray_recorder.end_subsegment()
        xray_recorder.end_segment()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)