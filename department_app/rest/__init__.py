from flask_restful import Resource
from flask import request, jsonify
from werkzeug.exceptions import HTTPException, BadRequest

from department_app import service
from department_app.models import Department, Employee

import logging
from datetime import datetime

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(module)s:%(message)s')

file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


# api classes
class DepartmentApi(Resource):
    """class for accessing Departments data through rest"""

    urls = [
        '/api/departments',
        '/api/departments/',
        '/api/departments/<int:department_id>',
        '/api/departments/<string:department_id>'
    ]

    def get(self, department_id=None):
        """get the department through restapi
           if the department's is not given then
           all the departments will be returned
           else the department with the specified if
           will be returned.
           return 404 if the department with the given
           id does not exist or return 400 if the type
           of the given id is not int

           department_id: the id of the department that will be returned
        """
        if department_id is None:
            deps = service.get_all(Department)
            response = jsonify({'departments': [dep.to_dict() for dep in deps]})
            return response.json, 200

        try:
            dep = service.get_or_404(Department, department_id)
        except HTTPException as e:
            logger.exception(e.description)
            return {'error': e.description}, e.code
        else:
            response = jsonify(dep.to_dict())
            return response.json, 200

    def post(self):
        """add a new department to the DB.
           if the name is not valid then
           the error message is returned
           if it is valid the departments
           gets added to the DB and return
           201 code with the department
        """
        try:
            name = request.form['dep_name']
            if not Department.validate_name(name):
                raise BadRequest("Invalid department's name")

            dep = Department(name=name.strip())
            service.insert_into_db(Department, dep)
        except HTTPException as e:
            logger.exception(e.description)
            return {'error': e.description}, e.code
        else:
            logger.info(f"Added {dep.name}")
            response = jsonify(dep.to_dict())
            return response.json, 201

    def put(self, department_id=None):
        """update the department with the given id.
           check if the new department's name is valid
           if not then return 400, if it is valid then
           return 200 and update the department

           department_id: the id of the department to updated
        """
        if department_id is None:
            return {'error': "id wasn't specified"}, 400

        try:
            dep = service.get_or_404(Department, department_id)
            new_name = request.form['dep_name']
            service.update_department_name(dep, new_name)
        except HTTPException as e:
            logger.exception(e.description)
            return {'error': e.description}, e.code
        else:
            logger.info(f"Updated {dep.name}")
            response = jsonify(dep.to_dict())
            return response.json, 200

    def delete(self, department_id=None):
        """delete the department with the given id.
           if the department does not exist return 404.
           if the type of the id is not int then return 400.
           if the department does exist then return 204 and
           delete it from the DB.

           department_id: the id of the department to delete
        """

        if department_id is None:
            return {'error': "id wasn't specified"}, 400

        try:
            dep = service.get_or_404(Department, department_id)
        except HTTPException as e:
            logger.exception(e.description)
            return {'error': e.description}, e.code
        else:
            service.delete_from_db(Department, dep)
            return '', 204


class EmployeeApi(Resource):
    """class for accessing Employeers data through rest"""

    urls = [
        '/api/employees',
        '/api/employees/',
        '/api/employees/<int:employee_id>',
        '/api/employees/<string:employee_id>'
    ]

    def get(self, employee_id=None):
        """get the employee information.
           if employee does not exist
           return 404, if the employee_id
           is not an integer then return 400.
           if the employee is presented in the DB
           then return json-formatted response and 200.
           if the employee_id is not specified then
           return all the employees.

           employee_id: the id of the employee to return
        """
        if employee_id is None:
            emps = service.get_all(Employee)
            response = jsonify({'employees': [emp.to_dict() for emp in emps]})
            return response.json, 200

        try:
            emp = service.get_or_404(Employee, employee_id)
        except HTTPException as e:
            logger.exception(e.description)
            return {'error': e.description}, e.code
        else:
            response = jsonify(emp.to_dict())
            return response.json, 200

    def post(self):
        """add a new employee to the DB.
           if the invalid fullname or invalid salary or
           invalid bday were given error message

           return a new employee and 201 code
        """
        try:
            fullname = request.form['fullname']
            bday = datetime.strptime(request.form['bday'], '%Y-%m-%d').date()

            try:
                dep_id = Department.query.filter_by(name=request.form['dep_name']).first().id
                salary = float(request.form['salary'])
            except ValueError:
                raise BadRequest('Salary must be numeric')
            except AttributeError:
                raise BadRequest(f"Unknown department {request.form['dep_name']}")

            if not Employee.validate_fullname(fullname):
                raise BadRequest("Invalid employee's name")

            emp = Employee(fullname=fullname, bday=bday,
                           salary=salary, department_id=dep_id)

            service.insert_into_db(Employee, emp)
            logger.info(f"Added employee - {emp.fullname}")
            response = jsonify(emp.to_dict())
            return response.json, 201

        except HTTPException as e:
            logger.exception(e)
            return {'error': e.description}, e.code

        except ValueError as e:
            logger.exception(e)
            return {'error': str(e)}, 400

    def put(self, employee_id=None):
        """update the employee with the given id.
           if the employee does not exist return 404.
           if the employee_id is not int return 400.
           if the employee exists then return 200 and
           the updated employee

           employee_id: the id of the employee to return
        """

        if employee_id is None:
            return {'error': "id wasn't specified"}, 400

        try:
            emp = service.get_or_404(Employee, employee_id)
            service.update_employee(emp, dict(request.form))
        except HTTPException as e:
            logger.exception(e.description)
            return {'error': e.description}, e.code
        except ValueError as e:
            logger.exception(e)
            return {'error': str(e)}, 400
        else:
            logger.info(f"Updated employee - {emp.fullname}")
            response = jsonify(emp.to_dict())
            return response.json, 200

    def delete(self, employee_id=None):
        """delete the employee with the given id
           if the employee does not exist return 404.
           if the employee_id has invalid type return 400.
           if employee exists then delete him and return 204
        """

        if employee_id is None:
            return {'error': "id wasn't specified"}, 400

        try:
            emp = service.get_or_404(Employee, employee_id)
        except HTTPException as e:
            logger.exception(e.description)
            return {'error': e.description}, e.code
        else:
            logger.info(f"Deleted employee - {emp.fullname}")
            service.delete_from_db(Employee, emp)
            return '', 204
