import os
import boto3
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_cors import CORS
from models import db, Trade
import logging
import watchtower
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# Initialize Flask app
app = Flask(__name__)

# Configure CloudWatch logging
if 'LOG_GROUP_NAME' in os.environ:
    region = os.environ.get('AWS_REGION', 'ap-southeast-1')
    logs_client = boto3.client('logs', region_name=region)
    
    handler = watchtower.CloudWatchLogHandler(
        log_group_name=os.environ.get('LOG_GROUP_NAME', '/trading-app/trade-service'),
        boto3_client=logs_client
    )
    
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info(f"CloudWatch logging configured for trade-service")

# Configure X-Ray recorder
xray_recorder.configure(
    service='your-service-name',
    daemon_address='xray-daemon:2000',
    sampling=True,
    context_missing='LOG_ERROR'
)

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

@app.route('/trades', methods=['GET', 'POST'])
def trades():
    if request.method == 'POST':
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
            return jsonify({'error': error_msg}), 400
        except Exception as e:
            # Handle other errors (roll back transaction)
            error_msg = f"Failed to create trade: {str(e)}"
            app.logger.error(error_msg, exc_info=True)
            db.session.rollback()
            return jsonify({'error': error_msg}), 500
    else:
        # Handle GET request
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)