from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    trade_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    trader_id = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"<Trade {self.id}: {self.asset_name}>"