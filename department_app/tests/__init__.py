"""tests"""
from department_app import create_app, db
from department_app.config import TestConfig


def create_test_app():
    """create app for tests"""
    app = create_app(app_config=TestConfig)
    with app.app_context():
        db.create_all()
    return app
