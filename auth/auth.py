from flask_restx import Resource, Namespace, fields
from flask import request
from models.users import Users
from werkzeug .security import generate_password_hash, check_password_hash
from http import HTTPStatus

auth_namespace = Namespace('auth', description='Api for Authentication')
register_model = auth_namespace.model(
    'Users', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description="Username"),
        'email': fields.String(required=True, description="Email"),
        'password': fields.String(required=True, description="Password"),
    }
)


@auth_namespace.route('/login')
class Login(Resource):
    def post(self):
        pass


@auth_namespace.route('/register')
class Register(Resource):
    @auth_namespace.expect(register_model)
    @auth_namespace.marshal_with(register_model)
    def post(self):
        req = request.get_json()
        user = Users(
            username=req.get('username'),
            password=generate_password_hash(req.get('password')),
            email=req.get('email'),
        )
        # user.save()

        return type(user), HTTPStatus.CREATED


@auth_namespace.route('/logout')
class Logout(Resource):
    def post(self):
        pass


@auth_namespace.route('/refresh')
class RefreshToken(Resource):
    def post(self):
        pass


@auth_namespace.route('/profile')
class GetProfile(Resource):
    def post(self):
        pass
