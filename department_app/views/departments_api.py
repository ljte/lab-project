from typing import Optional, Sequence, Tuple, Union, Dict, Any

from flask import request

from ..database.models import Department
from ..domain.exceptions import RecordNotFoundError
from ..domain.helpers import get_service
from ..domain.schemas import DepartmentSchema
from ..domain.schemas import DepartmentSchemaDB as schema
from .resource import Resource


def parse_dep(dep: Department) -> Dict[str, Any]:
    return {
        "id": dep.id,
        "name": dep.name,
        "avg_salary": dep.avg_salary,
        "num_of_employees": len(dep.employees)
    }


class DepartmentApi(Resource):
    @staticmethod
    def get(
        dep_id: Optional[int] = None
    ) -> Tuple[Union[Sequence[schema], schema], int]:
        service = get_service()
        if dep_id is None:
            return [schema.parse_obj(parse_dep(d)) for d in service.all(Department)], 200

        if not (dep := service.get(Department, id=dep_id)):
            raise RecordNotFoundError(f"Department with id `{dep_id} was not found")
        return schema.parse_obj(parse_dep(dep)), 200

    @staticmethod
    def post() -> Tuple[str, int]:
        dep = DepartmentSchema.parse_obj(request.form)
        get_service().insert(Department(**dep.dict()))
        return "", 201

    @staticmethod
    def put(dep_id: int) -> Tuple[str, int]:
        fields = DepartmentSchema.parse_obj(request.form)
        service = get_service()
        service.update(service.get(Department, id=dep_id), **fields.dict())
        return "", 204

    @staticmethod
    def delete(dep_id: int) -> Tuple[str, int]:
        service = get_service()
        service.delete(service.get(Department, id=dep_id))
        return "", 204
