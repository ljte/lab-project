"""restfull services"""

from flask import Blueprint
from flask_restful import Api

from department_app.rest.department_api import DepartmentApi
from department_app.rest.employee_api import EmployeeApi, FilterBday, FilterByDatePeriod


rest_blueprint = Blueprint('rest_api', __name__)

api = Api(rest_blueprint)

api.add_resource(DepartmentApi, *DepartmentApi.urls)
api.add_resource(EmployeeApi, *EmployeeApi.urls)
api.add_resource(FilterBday, *FilterBday.urls)
api.add_resource(FilterByDatePeriod, *FilterByDatePeriod.urls)
