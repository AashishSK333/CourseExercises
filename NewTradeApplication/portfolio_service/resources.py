from flask_restful import Resource, reqparse
from models import db, Trade

class PortfolioResource(Resource):
    def get(self, user_id):
        trades = Trade.query.filter_by(trader_id=user_id).all()
        # Compute portfolio values dynamically
        return [{'id': trade.id, 'asset_name': trade.asset_name, 'quantity': trade.quantity, 'price': trade.price, 'trade_time': trade.trade_time.isoformat()} for trade in trades]

class RebalanceResource(Resource):
    def post(self):
        # Implement rebalancing logic
        return {'message': 'Portfolio rebalanced successfully'}