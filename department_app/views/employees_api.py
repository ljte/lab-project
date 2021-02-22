from typing import Any, Dict, Tuple, Union, Sequence
from datetime import datetime

from flask import request

from ..database.models import Employee
from ..domain.exceptions import RecordNotFoundError
from ..domain.helpers import get_service
from ..domain.schemas import EmployeeSchema
from ..domain.schemas import EmployeeSchemaDB as schema
from .resource import Resource


def parse_employee(emp: Dict[str, Any]) -> Dict[str, Any]:
    parsed = {}
    for k, v in EmployeeSchema.parse_obj(emp).dict().items():
        if v is not None:
            parsed[k] = v
    return parsed


class EmployeeApi(Resource):
    @staticmethod
    def get(emp_id: int = None) -> Tuple[Union[Sequence[schema], schema], int]:
        service = get_service()
        if emp_id is None:
            emps = [schema.from_orm(e) for e in service.all(Employee)]
            return emps, 200

        if not (emp := service.get(Employee, id=emp_id)):
            raise RecordNotFoundError(f"Employee with id `{emp_id}` was not found")

        return schema.from_orm(emp), 200

    @staticmethod
    def post() -> Tuple[str, int]:
        emp = parse_employee(request.form)
        get_service().insert(Employee(**emp))
        return "", 201

    @staticmethod
    def put(emp_id: int) -> Tuple[str, int]:
        service = get_service()
        fields = parse_employee(request.form)
        service.update(service.get(Employee, id=emp_id), **fields)
        return "", 201

    @staticmethod
    def delete(emp_id: int) -> Tuple[str, int]:
        service = get_service()
        service.delete(service.get(Employee, id=emp_id))
        return "", 201
