import logging
from datetime import datetime

from flask_restful import Resource
from flask import request, jsonify
from werkzeug.exceptions import HTTPException, BadRequest

from department_app import service
from department_app.models import Department, Employee


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
        """get the department with the specified id.
           if department does not exist return 404,
           if department_id is not int return 400,
           if department_id is None return the list
           of all the departments

           department_id: the id of department to return
        """
        if department_id is None:
            deps = service.get_all(Department)
            response = jsonify({'departments':
                                [dep.to_dict() for dep in deps]})
            return response.json, 200

        try:
            dep = service.get_or_404(Department, id=department_id)
        except HTTPException as exc:
            logger.exception(exc.description)
            return {'message': exc.description}, exc.code
        else:
            response = jsonify(dep.to_dict())
            return response.json, 200

    def post(self):
        """insert the new department into the db.
           if department already exists return 400,
           if department's name is not valid return 400.
           else add the department and return 201
        """

        try:
            name = request.form['name']
            if Department.validate_name(name):
                try:
                    dep_id = request.form['id']
                except KeyError:
                    dep_id = service.get_id(Department)

                dep = Department(id=dep_id, name=name)
                service.insert_into_db(dep)
            else:
                raise BadRequest("invalid department's name '%s'" % name)
        except KeyError:
            return {'message': "Please specify department's name"}, 400
        except HTTPException as exc:
            logger.exception(exc.description)
            return {'message': exc.description}, exc.code
        else:
            logger.info('Added %s' % dep)
            response = jsonify(dep.to_dict())
            return response.json, 201

    def put(self, department_id=None):
        """update the department's name.
           if department_id is None return 400,
           if department_id is not int return 404,
           if department does not exist return 404,
           else update  the department and return 204

           department_id: the id of the department that is going to be updated
        """
        if department_id is None:
            return {'message': "Please specify the department's id"}, 400

        try:
            name = request.form['name']
            if Department.validate_name(name):
                dep = service.get_or_404(Department, id=department_id)
                service.update_record(Department, dep, **request.form)
            else:
                raise BadRequest("invalid department's name %s" % name)
        except KeyError:
            return {'message': "Please specify the department's name"}, 400
        except HTTPException as exc:
            logger.exception(exc.description)
            return {'message': exc.description}, exc.code
        else:
            logger.info('Updated %s' % dep)
            return '', 204

    def delete(self, department_id=None):
        """delete department with the given id.
           if department does not exist return 404,
           if department_id in not int return 404,
           else delete the department and return 204

           department_id: the id of the department that is going to be deleted
        """

        if department_id is None:
            return {'message': "Please specify the department's id"}, 400

        try:
            dep = service.get_or_404(Department, id=department_id)
        except HTTPException as exc:
            logger.exception(exc.description)
            return {'message': exc.description}, exc.code
        else:
            logger.info('Deleted %s' % dep)
            service.delete_from_db(dep)
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
        """get the employee with the specified id.
           if employee does not exist return 404,
           if employee_id is not int return 400,
           if employee_id is None return the list
           of all the employees

           employee_id: the id of department to return
        """
        if employee_id is None:
            emps = service.get_all(Employee)
            response = jsonify({'employees':
                                [emp.to_dict() for emp in emps]})
            return response.json, 200

        try:
            emp = service.get_or_404(Employee, id=employee_id)
        except HTTPException as exc:
            logger.exception(exc.description)
            return {'message': exc.description}, exc.code
        else:
            response = jsonify(emp.to_dict())
            return response.json, 200

    def post(self):
        """insert the new employee into the db.
           if employee already exists return 400,
           if employee's data is not valid return 400.
           else add the employee and return 201
        """

        try:
            # try to get all the necessary fields for posting a department
            # if something is missing then the KeyError is raised and gets processed
            fullname = request.form['fullname']
            bday = datetime.strptime(request.form['bday'], '%Y-%m-%d'),
            salary = float(request.form['salary'])
            dep_id = service.get_or_404(Department,
                                        name=request.form['dep_name']).id
            # validate the department's name
            if Employee.validate_fullname(fullname):
                # get the id if it was not given then just
                # set the id to be equal to the id of the last department + 1
                try:
                    emp_id = request.form['id']
                except KeyError:
                    emp_id = service.get_id(Employee)
                emp = Employee(
                    id=emp_id,
                    fullname=fullname,
                    bday=bday,
                    salary=salary,
                    department_id=dep_id
                )
                service.insert_into_db(emp)
            else:
                raise BadRequest("invalid employee's name '%s'" % fullname)

        except KeyError:
            return {'message': "Employee must have fullname, birthday, salary and department fields"}, 400

        except HTTPException as exc:
            logger.exception(exc.description)
            return {'message': exc.description}, exc.code

        except ValueError as exc:
            logger.exception(exc)
            return {'message': str(exc)}, 400

        else:
            logger.info('Added %s' % emp)
            response = jsonify(emp.to_dict())
            return response.json, 201

    def put(self, employee_id=None):
        """update the employee's name.
           if employee_id is None return 400,
           if employee_id is not int return 404,
           if employee does not exist return 404,
           else update  the employee and return 204

           employee_id: the id of the employee that is going to be updated
        """
        if employee_id is None:
            return {'message': "Please specify the employee's id"}, 400

        try:
            if Employee.validate_fullname(request.form['fullname']):
                emp = service.get_or_404(Employee, id=employee_id)
                service.update_record(Employee, emp, **request.form)
            else:
                return {'message': "invalid employee's fullname"}, 400

        except KeyError:
            return {'message': "invalid employee's fields"}, 400
        except HTTPException as exc:
            logger.exception(exc.description)
            return {'message': exc.description}, exc.code
        else:
            logger.info('Updated %s' % emp)
            return '', 204

    def delete(self, employee_id=None):
        """delete employee with the given id.
           if employee does not exist return 404,
           if employee_id in not int return 404,
           else delete the employee and return 204

           employee_id: the id of the employee that is going to be deleted
        """

        if employee_id is None:
            return {'message': "Please specify the employee's id"}, 400

        try:
            emp = service.get_or_404(Employee, id=employee_id)
        except HTTPException as exc:
            logger.exception(exc.description)
            return {'message': exc.description}, exc.code
        else:
            logger.info('Deleted %s' % emp)
            service.delete_from_db(emp)
            return '', 204
