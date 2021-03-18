from http import HTTPStatus

import psycopg2

from department_app.config import settings

from .resource import APIResource


class HealthcheckView(APIResource):
    http_method_names = ["get"]

    def get(self, request):
        postgres = settings.database
        try:
            psycopg2.connect(
                dbname=postgres.db,
                user=postgres.user,
                password=postgres.password,
                host=postgres.host,
                port=postgres.port,
            )
        except Exception as e:
            return {
                "message": f"Can not connect to the database: {e}"
            }, HTTPStatus.SERVICE_UNAVAILABLE
        return "", HTTPStatus.OK
