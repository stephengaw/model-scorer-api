import os
import secrets

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.scorer import Scorer, ScorerList, ScorerPredictWithList, ScorerPredictWithDict, ScorerTransformWithDict
from resources.user import UserRegister, User, UserAuth, TokenRefresh, UserRevoke
from revoked import REVOKED

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # changes the extensions tracker behaviour, not underlying SQLAlchemy behaviour
app.config['PROPAGATE_EXCEPTIONS'] = True  # for errors in JWT extended
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = secrets.token_hex(16)  # or app.config['JWT_SECRET_KEY']
api = Api(app)

jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:  # should use config file or database
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blacklist_loader
def token_in_blacklist_callback(decoded_jwt):
    return decoded_jwt['jti'] in REVOKED


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(_):
    return jsonify({
        'message': 'The token is invalid',
        'error': 'invalid_token'
    }), 422


@jwt.unauthorized_loader
def unauthorised_callback(_):
    return jsonify({
        'message': 'Authorisation required to access this resource.',
        'error': 'authorisation_required'
    }), 401


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return jsonify({
        'message': 'Require a fresh token to access this resource.',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'message': 'The token has been revoked.',
        'error': 'revoked_token'
    }), 401


api.add_resource(ScorerList, '/scorers')
api.add_resource(Scorer, '/scorers/<string:scorer_id>')
api.add_resource(ScorerPredictWithList, '/scorers/<string:scorer_id>/predict/list')
api.add_resource(ScorerPredictWithDict, '/scorers/<string:scorer_id>/predict/dict')
api.add_resource(ScorerTransformWithDict, '/scorers/<string:scorer_id>/transform/dict')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/users/<int:_id>')
api.add_resource(UserAuth, '/auth')
api.add_resource(UserRevoke, '/revoke')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5001, debug=True)
