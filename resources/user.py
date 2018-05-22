from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_refresh_token_required,
    get_raw_jwt
)
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp

from models.user import UserModel
from revoked import REVOKED

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', required=True, type=str, help='This field cannot be blank')
_user_parser.add_argument('password', required=True, type=str, help='This field cannot be blank')


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User already exists."}, 400

        UserModel(**data).save_to_db()

        return {"message": "User created successfully."}, 201


class User(Resource):
    @jwt_required
    def get(self, _id):

        user = UserModel.find_by_id(_id)

        if not user:
            return {"message": "Cannot find user."}, 404

        return user.json(), 200

    @jwt_required
    def delete(self, _id):

        user = UserModel.find_by_id(_id)

        if not user:
            return {"message": "Cannot find user."}, 404

        user.delete_from_db()

        return {"message": "User deleted."}, 200


class UserAuth(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       "access_token": access_token,
                       "refresh_token": refresh_token
                   }, 200

        return {"message": "Invalid credentials."}, 401


class UserRevoke(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        REVOKED.add(jti)
        return {
                   'message': 'Successfully revoked user token.'
               }, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user_id = get_jwt_identity()
        new_token = create_access_token(identity=current_user_id, fresh=False)
        return {'access_token': new_token}, 200
