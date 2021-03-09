FROM python:3.8-slim

RUN apt update && apt install gcc g++ libpq-dev -y
WORKDIR /app

COPY ./department_app /app
RUN python -m pip install -r requirements.txt

CMD python manage.py runserver 0:8000