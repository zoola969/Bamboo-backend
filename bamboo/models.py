import os
import re

from flask_login import UserMixin
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash

from bamboo import login_manager, app
from bamboo.extensions import db


class Coach(db.Model):
    UPLOAD_PATH = os.path.join(app.config['UPLOAD_FOLDER'], 'photos')
    DEFAULT_PHOTO = os.path.join(UPLOAD_PATH, 'default.png')

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64), default='')
    patronymic = db.Column(db.String(64), default='')
    description = db.Column(db.Text, nullable=True)
    photo = db.Column(db.String(256), default=DEFAULT_PHOTO)
    trainings = db.relationship('Training', backref='coach')
    individual_trainings = db.relationship('Register', backref='coach')

    @property
    def short_name(self):
        return ' '.join([self.first_name, self.last_name])

    @property
    def training_color(self):
        return self.color if self.color else self.DEFAULT_COLOR

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return ' '.join([self.last_name, self.first_name, self.patronymic])

    def to_json(self):
        return {
            'id': self.id,
            'name': self.short_name
        }


class Training(db.Model):
    # LEVELS
    ZERO = 'null_level'
    ANY = 'any_level'
    CONTINUOUS = 'continuous'

    LEVELS = (
        (ZERO, 'Уровень с нуля'),
        (ANY, 'Любой уровень'),
        (CONTINUOUS, 'Продолжающий уровень')
    )

    # Halls
    SMALL = 'small'
    MEDIUM = 'medium'
    BIG = 'big'

    HALLS = (
        (SMALL, 'Маленький'),
        (MEDIUM, 'Средний'),
        (BIG, 'Большой'),
    )

    id = db.Column(db.Integer, primary_key=True)
    coach_id = db.Column(db.Integer, db.ForeignKey('coach.id'), nullable=True)
    title = db.Column(db.String(64))
    start = db.Column(db.DateTime)
    stop = db.Column(db.DateTime)
    hall = db.Column(db.String(8), default=0)
    api_key = db.Column(db.String(128))
    level = db.Column(db.String(16), default='any_level')
    registers = db.relationship('Register', backref='training')

    @property
    def start_time(self):
        return self.start.strftime('%H:%M')

    @property
    def stop_time(self):
        return self.stop.strftime('%H:%M')

    @property
    def get_hall(self):
        for hall in self.HALLS:
            if self.hall == hall[0]:
                return hall[1]
        return ''

    @property
    def get_level(self):
        for level in self.LEVELS:
            if self.level == level[0]:
                return level[1]
        return self.ANY

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title.capitalize(),
            'coach': self.coach.short_name if self.coach else None,
            'level': self.get_level,
            'hall': self.get_hall,
            'start': self.start_time,
            'stop': self.stop_time,
        }

    def __repr__(self):
        coach = str(self.coach) if self.coach else ''
        return ' '.join([self.start.strftime('%Y-%m-%d %H:%M'), self.title, coach])


class Client(db.Model):
    INVALID_PHONE_NUMBER = 'Некорректный номер телефона'

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.BigInteger, index=True)
    name = db.Column(db.String(255))
    registers = db.relationship('Register', backref='client')

    @property
    def get_phone(self):
        phone = str(self.phone)
        return f'+7 ({phone[1:4]}) {phone[4:7]}-{phone[7:9]}-{phone[9:11]}'

    def __repr__(self):
        return ' '.join([self.get_phone, self.name])

    @validates('phone')
    def validate_phone(self, key, phone):
        """+79xxxxxxxxx"""
        phone = str(phone)
        if phone[0] != '+':
            phone = f'+{phone}'

        if phone[1] == '8':
            phone = f'+7{phone[2:]}'

        if len(phone) != 12 or not re.match(r'\+79[0-9]{9}', phone):
            raise AssertionError(self.INVALID_PHONE_NUMBER)
        return phone[1:]


class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    training_id = db.Column(db.Integer, db.ForeignKey('training.id'))
    individual_coach_id = db.Column(db.Integer, db.ForeignKey('coach.id'))

    def __repr__(self):
        coach = self.coach or self.training.coach
        coach = repr(coach)
        return ' '.join([self.training.start.strftime('%Y-%m-%d %H:%M'), self.training.title, coach])


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.Text())
    active = db.Column(db.Boolean, default=True)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        return self.active

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return self.authenticated

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_password(kwargs['password'])


@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))

