from flask import Flask

from .config import Config
from .database import Database


def create_app(config=Config()) -> Flask:
    app = Flask(__name__)
    app.config.update(config.dict())

    Database(config.DATABASE_URI).connect()

    @app.route("/")
    def index():
        return "))))"

    return app
