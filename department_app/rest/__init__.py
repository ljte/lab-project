"""restfull services"""

from flask import Blueprint
from flask_restful import Api

from department_app.rest.department_api import DepartmentApi
from department_app.rest.employee_api import EmployeeApi


rest_blueprint = Blueprint('rest_api', __name__)

errors = {
    'NotFound': {
        'message': 'The requested record was not found',
        'status': 404
    },
    'BadRequest': {
        'message': "Bad request. Please check your spelling and try again",
        'status': 400
    },
    'InvalidDepartmentName': {
        'message': "Invalid departments's name",
        'status': 400
    },
    'InvalidEmployeeName': {
        'message': "Invalid employee's fullname",
        'status': 400
    }
}

api = Api(rest_blueprint, errors=errors)

api.add_resource(DepartmentApi, *DepartmentApi.urls)
api.add_resource(EmployeeApi, *EmployeeApi.urls)
