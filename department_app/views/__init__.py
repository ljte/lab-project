from flask import Blueprint

from .departments_api import DepartmentApi
from .error_handlers import bad_request, resource_not_found

api_bp = Blueprint("api", __name__, url_prefix="/api")

view_func = DepartmentApi.as_view("department_api")

api_bp.add_url_rule("/departments/", view_func=view_func)
api_bp.add_url_rule(
    "/departments/<int:dep_id>", view_func=view_func, methods=["GET", "PUT", "DELETE"]
)
