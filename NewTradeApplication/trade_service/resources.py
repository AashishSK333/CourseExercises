from flask_restful import Resource, reqparse
from models import db, Trade

class TradeResource(Resource):
    def get(self, trade_id):
        trade = Trade.query.get_or_404(trade_id)
        return {'id': trade.id, 'trader_id': trade.trader_id, 'asset_name': trade.asset_name, 'quantity': trade.quantity, 'price': trade.price, 'trade_time': trade.trade_time.isoformat()}

class TradeListResource(Resource):
    def get(self):
        trades = Trade.query.all()
        return [{'id': trade.id, 'trader_id': trade.trader_id, 'asset_name': trade.asset_name, 'quantity': trade.quantity, 'price': trade.price, 'trade_time': trade.trade_time.isoformat()} for trade in trades]