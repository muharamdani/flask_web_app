from flask_restx import Resource, Namespace, fields
from flask import request
from models.users import Users
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest
from utils.response import response
from http import HTTPStatus
from sqlalchemy import exc
from flask_jwt_extended import \
    create_access_token,\
    create_refresh_token,\
    jwt_required,\
    get_jwt_identity

auth_namespace = Namespace('auth', description='Api for Authentication')
user_model = auth_namespace.model(
    'Users', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description="Username"),
        'email': fields.String(required=True, description="Email"),
        'password': fields.String(required=True, description="Password"),
        'created_at': fields.DateTime()
    }
)
#
# login_model = auth_namespace.model(
#     'Users', {
#         'email': fields.String(required=True, description="Email"),
#         'password': fields.String(required=True, description="Password"),
#     }
# )


@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(user_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            res = {
                'username': user.username,
                'email': user.email,
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
            return response.ok(res)
        else:
            values = "User not found"
            return response.not_found(values)


@auth_namespace.route('/register')
class Register(Resource):
    @auth_namespace.expect(user_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        req = request.get_json()
        username = req.get('username')
        password = req.get('password')
        email = req.get('email')
        user = Users(
            username=username,
            password=generate_password_hash(password),
            email=email,
        )
        try:
            user.save()
            return user, HTTPStatus.CREATED
        except exc.IntegrityError:
            user.rollback()
            raise BadRequest('User already registered!')


@auth_namespace.route('/refresh')
class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return response.ok(access_token)


@auth_namespace.route('/profile')
class GetProfile(Resource):
    @jwt_required()
    @auth_namespace.marshal_with(user_model)
    def get(self):
        identity = get_jwt_identity()
        user = Users.query.get_or_404(identity)
        return user, HTTPStatus.OK
