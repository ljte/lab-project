"""rest api for departments"""


from flask import request, jsonify
from flask_restful import Resource
from werkzeug.exceptions import HTTPException, BadRequest

from department_app.models.department import Department
from department_app.service import utils
from department_app.logger import logger


class DepartmentApi(Resource):
    """class for accessing Departments data through rest"""

    urls = [
        '/api/departments',
        '/api/departments/',
        '/api/departments/<int:department_id>'
    ]

    def get(self, department_id=None):
        """get the department with the specified id.
           if department does not exist return 404,
           if department_id is not int return 400,
           if department_id is None return the list
           of all the departments or the departments
           that are searched for by the search_string

           department_id: the id of department to return
        """
        if department_id is None:
            search_string = request.form.get('search_string', '')
            deps = utils.search_department_by_name(search_string)
            response = jsonify({'departments':
                                [dep.to_dict() for dep in deps]})
            return response.json, 200

        try:
            dep = utils.get_or_404(Department, id=department_id)
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
                dep = Department(name=name)
                utils.insert_into_db(dep)
            else:
                raise BadRequest("invalid department's name '%s'" % name)
        except KeyError:
            return {'message': "Please specify department's name"}, 400
        except HTTPException as exc:
            logger.exception(exc.description)
            return {'message': exc.description}, exc.code
        else:
            logger.info('Added %s', dep)
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
                dep = utils.get_or_404(Department, id=department_id)
                utils.update_record(Department, dep, **request.form)
            else:
                raise BadRequest("invalid department's name %s" % name)
        except KeyError:
            return {'message': "Please specify the department's name"}, 400
        except HTTPException as exc:
            logger.exception(exc.description)
            return {'message': exc.description}, exc.code
        else:
            logger.info('Updated %s', dep)
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
            dep = utils.get_or_404(Department, id=department_id)
        except HTTPException as exc:
            logger.exception(exc.description)
            return {'message': exc.description}, exc.code
        else:
            if dep.number_of_employees() != 0:
                return {'message': 'Can not delete department (Department must have 0 employees to be deleted)'}, 400
            logger.info('Deleted %s', dep)
            utils.delete_from_db(dep)
            return '', 204
