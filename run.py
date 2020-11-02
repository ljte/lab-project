from department_app import create_app, db
from department_app.tests import init_db_for_test
from department_app.config import TestConfig


def run(test=False):
    """method to run gunicorn"""
    if test:
        app = create_app(app_config=TestConfig)
        with app.app_context():
            db.create_all()
            init_db_for_test()
    else:
        app = create_app()
    return app


if __name__ == "__main__":
    app = run(test=True)
    app.run(debug=True)


