import os
import locale

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from bamboo.extensions import db


locale.setlocale(locale.LC_TIME, 'ru_RU')


def create_app():

    __config = {
        "development": "config.DevelopmentConfig",
        "testing": "config.TestingConfig",
        "production": "config.ProductionConfig"
    }

    app = Flask(__name__)
    config_name = os.getenv('FLASK_CONFIGURATION', 'development')
    app.config.from_object(__config[config_name])
    db.init_app(app)
    return app


app = create_app()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_view'

migrate = Migrate(app, db)


import bamboo.views, bamboo.models

if __name__ == '__main__':
    app.run(host='0.0.0.0')
