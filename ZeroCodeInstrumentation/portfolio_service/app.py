import os
import boto3
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from models import Trade, db
import logging
import watchtower
import sys
from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# Initialize X-Ray with proper daemon address
xray_recorder.configure(
    service='portfolio-service',
    daemon_address='xray-daemon:2000',
    context_missing='LOG_ERROR'
)
patch_all()  # Patch all supported libraries for X-Ray tracing

# Initialize Flask app
app = Flask(__name__)

# Configure CloudWatch logging with explicit region
if 'LOG_GROUP_NAME' in os.environ:
    # Explicitly get the region from environment variable
    region = os.environ.get('AWS_REGION', 'ap-southeast-1')
    
    # Create boto3 client with explicit region
    logs_client = boto3.client('logs', region_name=region)
    
    # Create handler with explicit client
    handler = watchtower.CloudWatchLogHandler(
        log_group_name=os.environ.get('LOG_GROUP_NAME', '/trading-app/portfolio-service'),
        boto3_client=logs_client
    )
    
    # Add the handler to your app's logger
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info(f"CloudWatch logging configured with region: {region}")

# Add X-Ray middleware to Flask
XRayMiddleware(app, xray_recorder)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db/trades'
db.init_app(app)
api = Api(app)
CORS(app)  # Enable CORS

# Health check endpoint for monitoring
#@app.route('/health')
#def health():
#    return {'status': 'healthy'}, 200

# Make sure this route exists and returns JSON
@app.route('/portfolio/<int:trader_id>', methods=['GET'])
def get_portfolio(trader_id):
    # Create a subsegment for X-Ray to track the portfolio calculation
    xray_recorder.begin_subsegment('calculate_portfolio')
    
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
        
        # Add metadata to the X-Ray trace
        xray_recorder.current_subsegment().put_metadata(
            'portfolio_stats', 
            {
                'trader_id': trader_id,
                'position_count': len(positions),
                'total_value': total_value
            },
            'trading_app'
        )
        
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
        xray_recorder.current_subsegment().add_exception(e, stack=sys.exc_info()[2])
        return jsonify({"error": error_msg}), 500
    finally:
        xray_recorder.end_subsegment()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)