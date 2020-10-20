from department_app import create_app


app = create_app()


def run():
    """method to run gunicorn"""
    return app


if __name__ == "__main__":
    app.run(debug=True)


