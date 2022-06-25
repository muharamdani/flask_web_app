from flask import Flask
from flask_restx import Api
from activity.activity import activity_namespace
from attend.attend import attend_namespace
from auth.auth import auth_namespace
from config.config import config_dict
from utils import db
from models.attend import Attendance
from models.activity import Activity
from models.users import Users
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, BadRequest


def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)
    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    api = Api(app, prefix='/api')
    api.add_namespace(activity_namespace)
    api.add_namespace(attend_namespace)
    api.add_namespace(auth_namespace)

    @api.errorhandler(NotFound)
    def not_found(err):
        return {
            'error': 'Not Found'
        }, 404

    @api.errorhandler(BadRequest)
    def bad_request(err):
        return {
            'error': 'Bad request'
        }, 400

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'Activity': Activity,
            'Attend': Attendance,
            'User': Users,
            'Migrate': migrate,
        }

    return app
