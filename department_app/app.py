from flask import Flask, g

from .config import Config
from .database import Database
from .views import bp as api_bp
from .views import resource_not_found


def create_app(config=Config()) -> Flask:
    app = Flask(__name__)
    app.config.update(config.dict())

    Database(config.DATABASE_URI).connect()

    @app.before_request
    def add_database_to_g():
        g.database = Database()

    @app.route("/")
    def index():
        print(g.database._url)
        return "HELLO, MISTER"

    app.register_blueprint(api_bp)

    app.register_error_handler(404, resource_not_found)

    return app
