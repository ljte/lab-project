from department_app import app


def run():
    """method to run gunicorn"""
    return app


if __name__ == "__main__":
    app.run(debug=True)


