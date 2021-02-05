from flask import Flask

from .models import db
from .config import BaseConfig


def create_app(config=BaseConfig)-> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    @app.route("/")
    def index():
        return "))))"

    return app