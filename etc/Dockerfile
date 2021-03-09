FROM python:3.8-slim

RUN apt update && apt install gcc g++ libpq-dev curl -y
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python \
    && cd /usr/local/bin \
    && ln -s /opt/poetry/bin/poetry

WORKDIR /app

COPY ./department_app ./

RUN poetry install --no-ansi --no-interaction

CMD poetry run gunicorn department_app.wsgi