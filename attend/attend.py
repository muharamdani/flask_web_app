from flask_restx import Resource, Namespace
attend_namespace = Namespace('attend', description='API List for attend')


@attend_namespace.route('/in')
class CheckIn(Resource):
    @staticmethod
    def get():
        return {'message': 'attend check in success'}


@attend_namespace.route('/out')
class CheckIn(Resource):
    @staticmethod
    def get():
        return {'message': 'attend check out success'}


@attend_namespace.route('/history')
class History(Resource):
    @staticmethod
    def get():
        return {'message': 'GET history attend'}
