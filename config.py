class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = '/opt/uploads'
    ALLOWED_EXTENSIONS = ['xls, xlsx']


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/pole_dance'
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

