from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, type=str, help='This field cannot be blank')
    parser.add_argument('password', required=True, type=str, help='This field cannot be blank')

    def post(self):

        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User already exists."}, 400

        UserModel(**data).save_to_db()

        return {"message": "User created successfully."}, 201


class User(Resource):

    @jwt_required()
    def get(self, _id):

        user = UserModel.find_by_id(_id)

        if not user:
            return {"message": "Cannot find user."}, 404

        return user.json(), 200

    @jwt_required()
    def delete(self, _id):

        user = UserModel.find_by_id(_id)

        if not user:
            return {"message": "Cannot find user."}, 404

        user.delete_from_db()

        return {"message": "User deleted."}, 200
