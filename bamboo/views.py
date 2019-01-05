import json
from datetime import datetime, timedelta
from random import randint

from flask import request, Response
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from bamboo import app
from bamboo.Trainings import Trainings
from bamboo.models import Training, Coach, Register, Client
from bamboo.extensions import db
from bamboo.messages import *
from bamboo.utils import JsonResponse


@app.route('/')
def hello_world():
    return 'Fuck you!'


@app.route('/au')
def b():
    name = request.args.get('name')
    phone = request.args.get('phone')
    try:
        db.session.add(Client(name=name, phone=phone))
    except AssertionError:
        return JsonResponse(Client.INVALID_PHONE_NUMBER, status=400)
    db.session.commit()
    return 'ok'


@app.route('/upload', methods=['POST'])
def upload_excel():
    file = request.files.get('file')
    if not file:
        return 'There is not file'


@app.route('/coach')
def coach_list_view():
    coach_list = [coach.to_json() for coach in Coach.query.all()]
    return JsonResponse(coach_list)


@app.route('/coach/<int:coach_id>')
def coach_view(coach_id):
    coach = Coach.query.get(coach_id)
    if not coach:
        return JsonResponse(COACH_DOES_NOT_EXIST, status=404)
    return JsonResponse(coach)


@app.route('/schedule', methods=['GET'])
def schedule_view():
    content = Trainings().to_table()
    return Response(json.dumps(content, ensure_ascii=False), status=200, content_type='application/json')


@app.route('/register', methods=['POST'])
def register_view():
    """
    phone: +7XXXXXXXXXX
    :return:
    """
    data = request.data
    if data:
        data = json.loads(data, encoding='utf-8')
    else:
        return JsonResponse(EMPTY_DATA, status=400)
    phone = data.get('phone')
    training_id = data.get('id')
    name = data.get('name')
    coach_id = data.get('coach_id')

    if not phone:
        return JsonResponse(MISSING_PHONE_NUMBER, status=400)
    elif not training_id:
        return JsonResponse(MISSING_TRAINING_ID, status=400)
    elif not name:
        return JsonResponse(MISSING_NAME, status=400)

    training = Training.query.get(training_id)
    if not training:
        return JsonResponse(TRAINING_DOES_NOT_EXIST, status=404)

    client = db.session.query(Client).filter_by(phone=phone).first()
    if not client:
        try:
            client = Client(phone=phone, name=name)
        except AssertionError as e:
            return JsonResponse(str(e), status=400)
        db.session.add(client)
        db.session.commit()

    if not training.coach_id and not coach_id:
        return JsonResponse(MISSING_COACH_ID, status=404)

    if db.session.query(Register.query.filter(Register.training_id == training_id,
                                              Register.client_id == client.id).exists()).scalar():
        return JsonResponse(RECORD_ALREADY_EXIST, status=400)

    db.session.add(Register(client_id=client.id,
                            training_id=training_id,
                            individual_coach_id=data.get('coach_id')))
    db.session.commit()
    return JsonResponse(SUCCESSFUL_RECORDING)


@app.route('/ac')
def ac():
    db.session.add(Coach(first_name='Маша', last_name='Нех', color='#fcb5b5'))
    db.session.add(Coach(first_name='Анастасия', color='#87bbc1'))
    db.session.add(Coach(first_name='Евгения', color='#8777a3'))
    db.session.add(Coach(first_name='Анна', color='#fffdba'))
    db.session.add(Coach(first_name='Кристина', color='#d8b06e'))
    db.session.add(Coach(first_name='Кристина', last_name='Шарм', color='#918284'))
    db.session.commit()
    return 'ok'


@app.route('/at')
def gay():
    now_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    training_names = ['POLEDANCE', 'ИДЕАЛЬНЫЙ ШПАГАТ', 'JAZZ FUNK', 'VOGUE']
    ids = [coach.id for coach in Coach.query.all()]
    ids.append(None)
    for i in range(7):
        for j in range(14):
            coach_id = ids[randint(0, len(ids) - 1)]
            title = training_names[randint(0, len(training_names) - 1)] if coach_id else 'ИНДИВИДУЛЬНОЕ ЗАНЯТИЕ'
            db.session.add(Training(coach_id=coach_id,
                                    title=title,
                                    start=now_date + timedelta(days=i, hours=j),
                                    stop=now_date + timedelta(days=i, hours=j + 1),
                                    hall=randint(0, 2)))
    db.session.commit()
    return 'ok'


admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(Coach, db.session))
admin.add_view(ModelView(Training, db.session))
admin.add_view(ModelView(Register, db.session))
