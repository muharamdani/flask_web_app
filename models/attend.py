from utils import db
from sqlalchemy import cast, DATE, and_
from datetime import datetime, date


class Attendance(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    is_attend = db.Column(db.Boolean(), default=True)
    checkin_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    checkout_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    def __repr__(self):
        return f"<Attend {self.user}>"

    @staticmethod
    def now():
        return db.func.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def is_checkin(self, user_id):
        return self.query.filter(
            Attendance.user_id == user_id,
            cast(Attendance.checkin_at, DATE) == date.today()
        ).first()

    def is_checkout(self, user_id):
        return self.query.filter(and_(
            Attendance.user_id == user_id,
            cast(Attendance.checkin_at, DATE) == date.today(),
            Attendance.checkout_at == None)
        ).first()

    @staticmethod
    def rollback():
        db.session.rollback()
