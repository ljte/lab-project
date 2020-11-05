"""rest api for employees"""

from datetime import datetime

from flask import request, jsonify
from flask_restful import Resource
from werkzeug.exceptions import HTTPException, BadRequest

from department_app.models.department import Department
from department_app.models.employee import Employee
from department_app.service import utils
from department_app.logger import logger


class EmployeeApi(Resource):
    """class for accessing Employeers data through rest"""

    urls = [
        '/api/employees',
        '/api/employees/',
        '/api/employees/<int:employee_id>',
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
            search_string = request.form.get('search_string', '')
            emps = utils.search_employees_by_fullname(search_string)
            response = jsonify({'employees':
                                [emp.to_dict() for emp in emps]})
            return response.json, 200

        try:
            emp = utils.get_or_404(Employee, id=employee_id)
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
            form = dict(request.form)
            fullname = form['fullname']
            bday = datetime.strptime(form['bday'], '%Y-%m-%d')
            salary = float(form['salary'])
            dep_id = utils.get_or_404(Department,
                                      name=form['dep_name']).id

            # validate the employee's name
            if Employee.validate_fullname(fullname):
                emp = Employee(
                    fullname=fullname,
                    bday=bday,
                    salary=salary,
                    department_id=dep_id
                )
                utils.insert_into_db(emp)
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
            logger.info('Added %s', emp)
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
            emp = utils.get_or_404(Employee, id=employee_id)
            form = dict(request.form)
            try:
                if Employee.validate_fullname(form['fullname']):
                    dep = utils.get_or_404(Department, name=form.get('department', emp.department.name))
                    form['department_id'] = dep.id
                    form.pop('department')
                    utils.update_record(Employee, emp, **form)
                else:
                    return {'message': "invalid employee's fullname"}, 400
            except KeyError:
                utils.update_record(Employee, emp, **form)

        except HTTPException as exc:
            logger.exception(exc.description)
            return {'message': exc.description}, exc.code
        else:
            logger.info('Updated %s', emp)
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
            emp = utils.get_or_404(Employee, id=employee_id)
        except HTTPException as exc:
            logger.exception(exc.description)
            return {'message': exc.description}, exc.code
        else:
            logger.info('Deleted %s', emp)
            utils.delete_from_db(emp)
            return '', 204


class FilterBday(Resource):
    """class for filtering employees by birthday
    """

    urls = [
        '/api/employees/filter_by_bday'
    ]

    def get(self):
        """get the employees with bday equal to the passed birthday
        as -d 'bday=1998-12-10' """
        form = dict(request.form)
        try:
            bday = datetime.strptime(form['bday'], "%Y-%m-%d").date()
            emps = utils.filter_employees_by_bday(bday)
        except KeyError:
            return {'message': 'Birthday was not given'}, 400
        except ValueError:
            return {'message': 'Birthday must have YY-MM-DD format'}, 400
        response = jsonify({'employees': [emp.to_dict() for emp in emps]})
        return response.json, 200


class FilterByDatePeriod(Resource):
    """class for filtering employees by date period
    """

    urls = [
        '/api/employees/filter_by_date_period'
    ]

    def get(self):
        """get the employees whose bdays fall into period from
        start_date to end_date
        """
        form = dict(request.form)
        try:
            start_date = datetime.strptime(form['start_date'], "%Y-%m-%d").date()
            end_date = datetime.strptime(form['end_date'], "%Y-%m-%d").date()
            emps = utils.filter_employees_by_date_period(start_date, end_date)
        except KeyError:
            return {'message': 'Invalid period'}, 400
        except ValueError:
            return {'message': 'Dates must have YY-MM-DD format'}, 400
        response = jsonify({'employees': [emp.to_dict() for emp in emps]})
        return response.json, 200
