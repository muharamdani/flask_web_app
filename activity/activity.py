from flask_restx import Resource, Namespace
activity_namespace = Namespace('activities', description='Namespace for activities')


@activity_namespace.route('/')
class Activity(Resource):
    @staticmethod
    def get():
        return {'message': 'get success'}

    @staticmethod
    def post():
        return {'message': 'post success'}


@activity_namespace.route('/<int:activity_id>')
class ActivityID(Resource):
    def put(self, activity_id):
        return {
            'message': 'put success',
            'activity_id': activity_id
        }

    def delete(self, activity_id):
        return {
            'message': 'delete success',
           'activity_id': activity_id
        }
