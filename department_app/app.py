from flask import Flask

from .database import Database
from .config import config


def create_app(config=config) -> Flask:
    app = Flask(__name__)
    app.config.update(config.dict())

    Database(config.DATABASE_URI).connect()

    @app.route("/")
    def index():
        return "))))"

    return app
