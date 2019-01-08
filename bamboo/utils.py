import json
import sys
from getpass import getpass

from flask import Response

from bamboo import app
from bamboo.models import User
from bamboo.extensions import db


def is_allowed_file(filename):
    if '.' in filename and filename.split('.')[-1] in app.config['ALLOWED_EXTENSIONS']:
        return True
    else:
        return False


class JsonResponse(Response):
    def __init__(self, content, mimetype='application/json', status=200):
        super().__init__(mimetype=mimetype)
        self.data = self.__content_handler(content)
        self.status_code = status

    @staticmethod
    def __content_handler(content):
        if isinstance(content, (list, dict)):
            content = json.dumps(content, ensure_ascii=False)
        elif isinstance(content, str):
            try:
                json.loads(content)
            except json.JSONDecodeError:
                content = json.dumps({'message': content}, ensure_ascii=False)
        else:
            content = JsonResponse.__content_handler(str(content))
        return content


def create_superuser():
    with app.app_context():
        if User.query.all():
            print('A user already exists! Create another? (y/n):')
            create = input()
            if create == 'n':
                sys.exit()

        print('Enter username: ')
        username = input()
        password = getpass()
        assert password == getpass('Password (again):')

        user = User(
            username=username,
            password=password)
        db.session.add(user)
        db.session.commit()
        print('User added.')
        sys.exit()
