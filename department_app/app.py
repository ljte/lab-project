from flask import Flask

from .config import BasicConfig


def create_app(config=BasicConfig)-> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    @app.route("/")
    def index():
        return "))))"

    return app
