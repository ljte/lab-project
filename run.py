from department_app import create_app


def run():
    """method to run gunicorn"""
    app = create_app()
    return app


if __name__ == "__main__":
    app = run()
    app.run(debug=True)


