from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from models import Trade, db
from resources import PortfolioResource, RebalanceResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db/trades'
db.init_app(app)
api = Api(app)
CORS(app)  # Enable CORS

#api.add_resource(PortfolioResource, '/portfolio/<int:user_id>')
#api.add_resource(RebalanceResource, '/portfolio/rebalance')


@app.route('/health')
def health():
    return {'status': 'healthy'}, 200


@app.before_request
def log_request():
    app.logger.debug(f"Request: {request.method} {request.path}")

@app.after_request
def log_response(response):
    app.logger.debug(f"Response: {response.status_code}, Content-Type: {response.content_type}")
    app.logger.debug(f"Response body: {response.get_data(as_text=True)[:200]}...")
    return response

# Make sure this route exists and returns JSON
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
        app.logger.error(f"Error calculating portfolio: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)