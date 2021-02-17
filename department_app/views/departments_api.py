from typing import Any, Dict, Optional, Sequence, Tuple, Union

from flask import abort
from flask.views import MethodView
from pydantic import ValidationError

from ..database import Database
from ..database.models import Department
from ..domain.schemas import DepartmentSchema
from ..service import DatabaseService
from .helpers import json_response

JSON = Union[Sequence[Dict[str, Any]], Dict[str, Any]]


class DepartmentApi(MethodView):
    def get(self, dep_id: Optional[int] = None) -> Tuple[JSON, int]:
        service = DatabaseService(Database())
        if dep_id is None:
            deps = [DepartmentSchema.from_orm(d) for d in service.all(Department)]
            json_response(deps)
        try:
            dep = DepartmentSchema.from_orm(service.get(Department, id=dep_id))
        except ValidationError:
            abort(404, description=f"Department with id `{dep_id}` was not found")
        return json_response(dep)
