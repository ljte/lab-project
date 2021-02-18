from flask import Blueprint

from .departments_api import DepartmentApi
from .employees_api import EmployeeApi
from .error_handlers import bad_request, resource_not_found

api_bp = Blueprint("api", __name__, url_prefix="/api")

dep_view = DepartmentApi.as_view("department_api")
emp_view = EmployeeApi.as_view("employee_api")

api_bp.add_url_rule("/departments/", view_func=dep_view)
api_bp.add_url_rule(
    "/departments/<int:dep_id>", view_func=dep_view, methods=["GET", "PUT", "DELETE"]
)

api_bp.add_url_rule("/employees/", view_func=emp_view)
api_bp.add_url_rule(
    "/employees/<int:emp_id>", view_func=emp_view, methods=["GET", "PUT", "DELETE"]
)
