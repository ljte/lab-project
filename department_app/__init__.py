"""application initialization"""

from flask import Flask
from flask_migrate import Migrate

from department_app.config import Config
from department_app.rest import rest_blueprint
from department_app.models import db


migrate = Migrate()


def create_app(app_config=Config):
    """basically it is an application factory"""

    # configure app
    app = Flask(__name__)
    app.config.from_object(app_config)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db, directory='department_app/migrations')

    # register blueprints
    app.register_blueprint(rest_blueprint)

    return app
