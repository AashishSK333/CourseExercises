from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trader_id = db.Column(db.Integer, nullable=False)
    asset_name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    trade_time = db.Column(db.DateTime, nullable=False)