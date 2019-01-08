from flask import url_for, request
from flask_admin import AdminIndexView, Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.utils import redirect
from wtforms import SelectField, validators

from bamboo import app
from bamboo.models import Training, Coach, Register, Client
from bamboo.extensions import db
from bamboo.validators import PhoneValidation


class CustomModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('login_view', next=request.url))


class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('login_view', next=request.url))


class TrainingAdminView(CustomModelView):
    form_overrides = dict(
        level=SelectField,
        hall=SelectField,
    )
    form_args = dict(
        level=dict(choices=Training.LEVELS),
        hall=dict(choices=Training.HALLS),
        title=dict(validators=[validators.Length(min=10, max=64), validators.DataRequired()]),
        start=dict(validators=[validators.DataRequired()]),
        stop=dict(validators=[validators.DataRequired()]),
        api_key=dict(validators=[validators.DataRequired()])
    )
    column_labels = dict(
        level='Уровень',
        hall='Зал',
        title='Название занятия',
        start='Начало занятия',
        stop='Конец занятия',
        coach='Тренер'
    )
    column_choices = dict(
        level=Training.LEVELS,
        hall=Training.HALLS
    )

    form_excluded_columns = ['registers']

    def __init__(self):
        super().__init__(Training, db.session, 'Занятия')


class CoachAdminView(CustomModelView):
    form_args = dict(
        first_name=dict(validators=[validators.DataRequired()]),
    )
    column_labels = dict(
        first_name='Имя',
        last_name='Фамилия',
        patronymic='Отчество',
        description='Описание'
    )

    form_excluded_columns = ['trainings', 'individual_trainings']

    def __init__(self):
        super().__init__(Coach, db.session, 'Тренеры')


class RegisterAdminView(CustomModelView):
    form_args = dict(
        training=dict(validators=[validators.DataRequired()]),
        client=dict(validators=[validators.DataRequired()]),
    )
    column_labels = dict(
        coach='Персональный тренер',
        training='Тренировка',
        client='Клиент',
    )

    def __init__(self):
        super().__init__(Register, db.session, 'Записи')


class ClientAdminView(CustomModelView):
    column_labels = dict(
        phone='Номер телефона',
        name='ФИО'
    )
    form_args = dict(
        phone=(dict(validators=[validators.DataRequired(), PhoneValidation()])),
        name=(dict(validators=[validators.DataRequired()]))
    )
    
    form_excluded_columns = ['registers']

    def __init__(self):
        super().__init__(Client, db.session, 'Клиенты')


admin = Admin(app, name='Bamboo', template_mode='bootstrap3', index_view=CustomAdminIndexView())
admin.add_views(CoachAdminView(), TrainingAdminView(), RegisterAdminView(), ClientAdminView())
