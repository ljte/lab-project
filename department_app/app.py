from flask import Flask

from .config import BaseConfig


def create_app(config=BaseConfig)-> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    @app.route("/")
    def index():
        return "))))"

    return app
