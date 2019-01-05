import re

from sqlalchemy.orm import validates

from bamboo.extensions import db


class Coach(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64), default='')
    patronymic = db.Column(db.String(64), default='')
    description = db.Column(db.Text, nullable=True)
    trainings = db.relationship('Training', backref='coach')
    individual_trainings = db.relationship('Register', backref='coach')

    @property
    def short_name(self):
        return ' '.join([self.first_name, self.last_name])

    def __repr__(self):
        return ' '.join([self.last_name, self.first_name, self.patronymic])

    def to_json(self):
        return {
            'id': self.id,
            'name': self.short_name
        }


class Training(db.Model):
    HALLS = (
        ('small', 'Маленький зал'),
        ('medium', 'Средний зал'),
        ('big', 'Большой зал'),
    )
    id = db.Column(db.Integer, primary_key=True)
    coach_id = db.Column(db.Integer, db.ForeignKey('coach.id'), nullable=True)
    title = db.Column(db.String(64))
    start = db.Column(db.DateTime)
    stop = db.Column(db.DateTime)
    hall = db.Column(db.String(32))
    registers = db.relationship('Register', backref='training')

    @property
    def start_time(self):
        return self.start.strftime('%H:%M')

    @property
    def stop_time(self):
        return self.stop.strftime('%H:%M')

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'coach': self.coach.short_name if self.coach else None,
            'hall': self.hall,
            'start': self.start_time,
            'stop': self.stop_time,
        }

    def __repr__(self):
        return ' '.join([self.start.strftime('%Y:%m:%d %H:%M'), self.title, self.coach])


class Client(db.Model):
    INVALID_PHONE_NUMBER = 'Некорректный номер телефона'

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.BigInteger, index=True)
    name = db.Column(db.String(255))
    registers = db.relationship('Register', backref='client')

    def __repr__(self):
        return ' '.join([str(self.phone), self.name])

    @validates('phone')
    def validate_phone(self, key, phone):
        """+79xxxxxxxxx"""
        if len(phone) != 12 or not re.match(r'\+79[0-9]{9}', phone):
            raise AssertionError(self.INVALID_PHONE_NUMBER)
        return phone[1:]


class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    training_id = db.Column(db.Integer, db.ForeignKey('training.id'))
    individual_coach_id = db.Column(db.Integer, db.ForeignKey('coach.id'))
