import os
import locale

from flask import Flask

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

import bamboo.views, bamboo.models
