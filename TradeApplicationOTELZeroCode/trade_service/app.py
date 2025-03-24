import os
import logging
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_cors import CORS
from models import db, Trade
from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# Initialize X-Ray with proper daemon address
xray_recorder.configure(
    service='trade-service',
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
app.logger.info("Trade service starting up")

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
    # Create a segment for this request
    segment = xray_recorder.begin_segment('trade-handler')
    
    if request.method == 'POST':
        subsegment = xray_recorder.begin_subsegment('create-trade')
        try:
            # Process the POST request
            data = request.json
            app.logger.info(f"Processing trade: {data}")
            
            # Add annotation to the X-Ray trace for filtering
            xray_recorder.put_annotation('trader_id', data['trader_id'])
            xray_recorder.put_annotation('asset_name', data['asset_name'])
            
            # Create a new trade
            new_trade = Trade(
                asset_name=data['asset_name'],
                quantity=float(data['quantity']),
                price=float(data['price']),
                trade_time=data['trade_time'],
                trader_id=int(data['trader_id'])
            )
            
            # Add to database and commit
            db.session.add(new_trade)
            db.session.commit()
            
            app.logger.info(f"Trade created successfully: {new_trade.id}")
            
            # Return the created trade
            return jsonify({
                'id': new_trade.id,
                'asset_name': new_trade.asset_name,
                'quantity': new_trade.quantity,
                'price': new_trade.price,
                'trade_time': new_trade.trade_time.isoformat(),
                'trader_id': new_trade.trader_id,
                'message': 'Trade created successfully'
            }), 201
            
        except Exception as e:
            app.logger.error(f"Error creating trade: {str(e)}")
            db.session.rollback()
            xray_recorder.add_exception(e)
            return jsonify({'error': f'Failed to create trade: {str(e)}'}), 500
        finally:
            xray_recorder.end_subsegment()
            
    else:
        # Handle GET request
        subsegment = xray_recorder.begin_subsegment('list-trades')
        try:
            trades = Trade.query.all()
            app.logger.info(f"Retrieved {len(trades)} trades")
            xray_recorder.end_subsegment()
            return jsonify([{
                'id': trade.id,
                'trader_id': trade.trader_id, 
                'asset_name': trade.asset_name, 
                'quantity': trade.quantity, 
                'price': trade.price, 
                'trade_time': trade.trade_time.isoformat()
            } for trade in trades])
        except Exception as e:
            app.logger.error(f"Error retrieving trades: {str(e)}")
            xray_recorder.add_exception(e)
            return jsonify({'error': f'Failed to retrieve trades: {str(e)}'}), 500
        finally:
            xray_recorder.end_subsegment()
    
    xray_recorder.end_segment()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)