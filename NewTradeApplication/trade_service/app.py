from flask import Flask, request, jsonify
from flask_restful import Api
from flask_cors import CORS
from models import db, Trade
from resources import TradeResource, TradeListResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db/trades'
db.init_app(app)
api = Api(app)
CORS(app)  # Enable CORS

# Create tables if they don't exist
with app.app_context():
    db.create_all()

#api.add_resource(TradeResource, '/trades/<int:trade_id>')
#api.add_resource(TradeListResource, '/trades')

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

@app.route('/trades', methods=['GET', 'POST'])
def trades():
    if request.method == 'POST':
        # Process the POST request
        data = request.json
        
        try:
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
            return jsonify({'error': f'Missing required field: {str(e)}'}), 400
        except Exception as e:
            # Handle other errors (roll back transaction)
            db.session.rollback()
            return jsonify({'error': f'Failed to create trade: {str(e)}'}), 500
    else:
        # Handle GET request by delegating to the TradeListResource
        trades = Trade.query.all()
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