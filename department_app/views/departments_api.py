from typing import Any, Dict, Optional, Sequence, Tuple, Union

from flask import request
from flask.views import MethodView

from ..database.models import Department
from ..domain.exceptions import RecordNotFoundError
from ..domain.helpers import get_service
from ..domain.schemas import DepartmentSchema, DepartmentSchemaDB
from .helpers import json_response

JSON = Union[Sequence[Dict[str, Any]], Dict[str, Any]]


class DepartmentApi(MethodView):
    def get(self, dep_id: Optional[int] = None) -> Tuple[JSON, int]:
        service = get_service()
        if dep_id is None:
            deps = [DepartmentSchemaDB.from_orm(d) for d in service.all(Department)]
            return json_response(deps)
        try:
            if not (dep := service.get(Department, id=dep_id)):
                raise RecordNotFoundError(f"Department with id `{dep_id} was not found")
            dep_schema = DepartmentSchemaDB.from_orm(dep)
        except Exception as e:
            return json_response(e, 400)
        return json_response(dep_schema)

    def post(self) -> Tuple[Union[str, JSON], int]:
        try:
            dep = DepartmentSchema.parse_obj(request.form)
            get_service().insert(Department(**dep.dict()))
        except Exception as e:
            return json_response(e, 400)

        return "", 201
