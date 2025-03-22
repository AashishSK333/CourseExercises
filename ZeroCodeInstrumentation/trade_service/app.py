import os
import boto3
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_cors import CORS
from models import db, Trade
import logging
import watchtower
import sys
from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# Initialize X-Ray with proper daemon address
xray_recorder.configure(
    service='trade-service',  # or 'portfolio-service'
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
        log_group_name=os.environ.get('LOG_GROUP_NAME', '/trading-app/trade-service'),
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

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Health check endpoint for monitoring
#@app.route('/health')
#def health():
#    return {'status': 'healthy'}, 200

@app.route('/trades', methods=['GET', 'POST'])
def trades():
    if request.method == 'POST':
        # Create a subsegment for X-Ray to track the trade creation process
        xray_recorder.begin_subsegment('create_trade')
        try:
            # Process the POST request
            data = request.json
            app.logger.info(f"Processing trade: {data}")
            
            # Create a new trade object
            new_trade = Trade(
                asset_name=data['asset_name'],
                quantity=data['quantity'],
                price=data['price'],
                trade_time=data['trade_time'],
                trader_id=data['trader_id']
            )
            
            # Add to database and commit
            db.session.add(new_trade)
            db.session.commit()
            
            app.logger.info(f"Trade created successfully: {new_trade.id}")
            
            # Return the created trade with 201 Created status
            return jsonify({
                'id': new_trade.id,
                'asset_name': new_trade.asset_name,
                'quantity': new_trade.quantity,
                'price': new_trade.price,
                'trade_time': new_trade.trade_time.isoformat(),
                'trader_id': new_trade.trader_id,
                'message': 'Trade created successfully'
            }), 201
            
        except KeyError as e:
            # Handle missing fields
            error_msg = f"Missing required field: {str(e)}"
            app.logger.error(error_msg)
            xray_recorder.current_subsegment().add_error_flag()
            return jsonify({'error': error_msg}), 400
        except Exception as e:
            # Handle other errors (roll back transaction)
            error_msg = f"Failed to create trade: {str(e)}"
            app.logger.error(error_msg, exc_info=True)
            db.session.rollback()
            xray_recorder.current_subsegment().add_exception(e, stack=sys.exc_info()[2])
            return jsonify({'error': error_msg}), 500
        finally:
            xray_recorder.end_subsegment()
    else:
        # Handle GET request
        subsegment = xray_recorder.begin_subsegment('list_trades')
        try:
            trades = Trade.query.all()
            app.logger.info(f"Retrieved {len(trades)} trades")
            return jsonify([{
                'id': trade.id, 
                'trader_id': trade.trader_id, 
                'asset_name': trade.asset_name, 
                'quantity': trade.quantity, 
                'price': trade.price, 
                'trade_time': trade.trade_time.isoformat()
            } for trade in trades])
        finally:
            xray_recorder.end_subsegment()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)