from flask import Flask, g

from department_app.service import DatabaseService

from .config import Config
from .database import Database
from .views import api_bp, resource_not_found


def create_app(config=Config()) -> Flask:
    app = Flask(__name__)
    app.config.update(config.dict())

    db = Database(config)
    db.connect()

    @app.before_request
    def add_objects_to_g():
        g.database = db
        g.service = DatabaseService(db)

    @app.route("/")
    def index():
        print(g.database._url)
        return "HELLO, MISTER"

    app.register_blueprint(api_bp)

    app.register_error_handler(404, resource_not_found)

    return app
