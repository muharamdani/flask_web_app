from dateutil import parser
from flask_restx import Resource, Namespace, fields
from flask import request
from utils import db
from http import HTTPStatus
from utils.response import response
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.activity import Activity
from sqlalchemy import cast, DATE
from werkzeug.exceptions import BadRequest, UnprocessableEntity

activity_namespace = Namespace('activities', description='Namespace for activities')
activity_model = activity_namespace.model(
    'Activities', {
        'id': fields.Integer(),
        'user_id': fields.Integer(required=True),
        'activity': fields.String(required=True),
        'created_at': fields.DateTime(),
        'updated_at': fields.DateTime(),
    }
)


@activity_namespace.route('/')
class ActivityData(Resource):
    @jwt_required()
    @activity_namespace.marshal_with(activity_model)
    def get(self):
        user_id = get_jwt_identity()
        Activity().allow_access(user_id)

        req = request.args
        filter_date = req.get('date')
        if filter_date:
            try:
                filter_date = parser.parse(filter_date).date()
                activities = Activity.query.filter(
                    Activity.user_id == user_id,
                    cast(Activity.created_at, DATE) == filter_date
                ).all()
                return activities, HTTPStatus.OK
            except Exception as e:
                raise BadRequest("Invalid date format")
        else:
            activities = Activity.query.filter(Activity.user_id == user_id).all()
            return activities, HTTPStatus.OK

    @jwt_required()
    @activity_namespace.expect(activity_model)
    @activity_namespace.marshal_with(activity_model)
    def post(self):
        # CheckIn validation
        user_id = get_jwt_identity()
        Activity().allow_access(user_id)

        req = activity_namespace.payload
        activity = req.get('activity')
        if not activity:
            raise UnprocessableEntity('Activity is required')

        activity = Activity(
            user_id=user_id,
            activity=activity
        )
        activity.save()
        return activity, HTTPStatus.OK


@activity_namespace.route('/<int:activity_id>')
class ActivityID(Resource):
    @jwt_required()
    @activity_namespace.marshal_with(activity_model)
    def get(self, activity_id):
        user_id = get_jwt_identity()
        Activity().allow_access(user_id)
        activity = Activity.get_by_id(activity_id)
        return activity, HTTPStatus.OK

    @jwt_required()
    @activity_namespace.expect(activity_model)
    @activity_namespace.marshal_with(activity_model)
    def put(self, activity_id):
        user_id = get_jwt_identity()
        Activity().allow_access(user_id)

        req = activity_namespace.payload
        activity_by_id = Activity.get_by_id(activity_id)
        activity_by_id.activity = req.get('activity')
        db.session.commit()
        return activity_by_id, HTTPStatus.OK

    @jwt_required()
    def delete(self, activity_id):
        user_id = get_jwt_identity()
        Activity().allow_access(user_id)
        Activity.get_by_id(activity_id).delete()
        return response.ok('Delete success')
