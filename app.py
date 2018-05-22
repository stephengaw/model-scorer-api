import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.scorer import Scorer, ScorerList, ScorerPredictWithList, ScorerPredictWithDict, ScorerTransformWithDict
from resources.user import UserRegister, User, UserAuth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # changes the extensions tracker behaviour, not underlying SQLAlchemy behaviour
app.config['PROPAGATE_EXCEPTIONS'] = True  # for errors in JWT extended
app.secret_key = 'stephen'  # or app.config['JWT_SECRET_KEY']
api = Api(app)

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:  # should use config file or database
        return {'is_admin': True}
    return {'is_admin': False}

api.add_resource(ScorerList, '/scorers')
api.add_resource(Scorer, '/scorers/<string:scorer_id>')
api.add_resource(ScorerPredictWithList, '/scorers/<string:scorer_id>/predict/list')
api.add_resource(ScorerPredictWithDict, '/scorers/<string:scorer_id>/predict/dict')
api.add_resource(ScorerTransformWithDict, '/scorers/<string:scorer_id>/transform/dict')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/users/<int:_id>')
api.add_resource(UserAuth, '/auth')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5001, debug=True)
