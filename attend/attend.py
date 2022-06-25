from datetime import datetime
from flask_restx import Resource, Namespace, fields
from utils import db
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.response import response
from models.attend import Attendance
attend_namespace = Namespace('attend', description='API List for attend')
attend_model = attend_namespace.model(
    'Attend', {
        'id': fields.Integer(),
        'user_id': fields.Integer(),
        'is_attend': fields.Boolean(),
        'checkin_at': fields.DateTime(),
        'checkout_at': fields.DateTime(),
    }
)


@attend_namespace.route('/in')
class CheckIn(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        attendance = Attendance().is_checkin(user_id)
        if not attendance:
            checkin_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            attend = Attendance(user_id=user_id)
            attend.save()
            res = {
                'user_id': user_id,
                'is_attend': True,
                'checkin_at': checkin_date,
            }
            return response.ok(res)
        return response.bad_request('Already check in today!')


@attend_namespace.route('/out')
class CheckOut(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        attendance = Attendance().is_checkout(user_id)
        if attendance:
            checkout_date = Attendance.now()
            attendance.checkout_at = checkout_date
            attendance.is_attend = False
            db.session.commit()

            checkout_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            res = {
                'user_id': user_id,
                'is_attend': False,
                'checkout_at': checkout_date,
            }
            return response.ok(res)
        return response.bad_request('Check in first, or user already check out!')


@attend_namespace.route('/history')
class History(Resource):
    @jwt_required()
    @attend_namespace.marshal_with(attend_model)
    def get(self):
        user_id = get_jwt_identity()
        attendances = Attendance.query.filter(Attendance.user_id == user_id).all()
        return attendances, HTTPStatus.OK
