from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from models import db
from resources import PortfolioResource, RebalanceResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db/trades'
db.init_app(app)
api = Api(app)
CORS(app)  # Enable CORS

api.add_resource(PortfolioResource, '/portfolio/<int:user_id>')
api.add_resource(RebalanceResource, '/portfolio/rebalance')

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)