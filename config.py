import os


class Config(object):
    SECRET_KEY = b'(\xd4\xaf0\x96\x0b\r\xce\xa0\xa7\x9e\xe0\x1d\x82`\xb6'
    DEBUG = False
    TESTING = False
    DATABASE_NAME = os.environ.get('DB_NAME')
    DATABASE_USER = os.environ.get('DB_USER')
    DATABASE_PASSWORD = os.environ.get('DB_PASSWORD')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@localhost/{DATABASE_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = '/opt/uploads'
    ALLOWED_EXTENSIONS = ['xls, xlsx']


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

