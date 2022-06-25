from utils import db
from models.attend import Attendance
from werkzeug.exceptions import Forbidden


class Activity(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    activity = db.Column(db.Text())
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    def __repr__(self):
        return f"<Activity {self.user}>"

    @staticmethod
    def allow_access(user_id):
        attend = Attendance().is_checkin(user_id)
        if not attend:
            raise Forbidden("Please check in first")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, activity_id):
        return cls.query.get_or_404(activity_id)
