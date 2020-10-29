from department_app import create_app
from department_app.config import TestConfig


def run(test=False):
    """method to run gunicorn"""
    if test:
        app = create_app(app_config=TestConfig)
    else:
        app = create_app()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)


