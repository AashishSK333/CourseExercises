import os
import boto3
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_cors import CORS
from models import Trade, db
import logging
import watchtower
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# Initialize Flask app
app = Flask(__name__)

# Configure X-Ray recorder
xray_recorder.configure(
    service='your-service-name',
    daemon_address='xray-daemon:2000',
    sampling=True,
    context_missing='LOG_ERROR'
)

# Apply X-Ray middleware to your Flask app
XRayMiddleware(app, xray_recorder)

# Configure CloudWatch logging
if 'LOG_GROUP_NAME' in os.environ:
    region = os.environ.get('AWS_REGION', 'ap-southeast-1')
    logs_client = boto3.client('logs', region_name=region)
    
    handler = watchtower.CloudWatchLogHandler(
        log_group_name=os.environ.get('LOG_GROUP_NAME', '/trading-app/portfolio-service'),
        boto3_client=logs_client
    )
    
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info(f"CloudWatch logging configured for portfolio-service")

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db/trades'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)
CORS(app)

# Portfolio endpoint
@app.route('/portfolio/<int:trader_id>', methods=['GET'])
def get_portfolio(trader_id):
    try:
        # Debug log
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
        
        # Format response and explicitly specify content type
        response = jsonify({
            "trader_id": trader_id,
            "positions": position_list,
            "total_value": total_value
        })
        response.headers["Content-Type"] = "application/json"
        return response
        
    except Exception as e:
        error_msg = f"Error calculating portfolio: {str(e)}"
        app.logger.error(error_msg, exc_info=True)
        return jsonify({"error": error_msg}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5002)