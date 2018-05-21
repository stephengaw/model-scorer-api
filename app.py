import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.scorer import Scorer, ScorerList, ScorerPredictWithList, ScorerPredictWithDict, ScorerTransformWithDict
from resources.user import UserRegister

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # changes the extensions tracker behaviour, not underlying SQLAlchemy behaviour
app.secret_key = 'stephen'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(ScorerList, '/scorers')
api.add_resource(Scorer, '/scorers/<string:scorer_id>')
api.add_resource(ScorerPredictWithList, '/scorers/<string:scorer_id>/predict/list')
api.add_resource(ScorerPredictWithDict, '/scorers/<string:scorer_id>/predict/dict')
api.add_resource(ScorerTransformWithDict, '/scorers/<string:scorer_id>/transform/dict')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5001, debug=True)
