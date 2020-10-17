from datetime import date

from werkzeug.exceptions import BadRequest
import requests

from department_app import db
from department_app.models import Department, Employee


def get_all(model):
    """get all the records in the model table.

       model: db.Model that maps to some table in the DB
    """
    return model.query.all()


def get_or_404(model, record_id):
    """get the record with the id of record_id
       from the model or raise NotFound Exception
       if the record with the given id has not been found.
       Raise the BadRequest exception if the record_id is
       not an integer.

       model: db.Model that maps to some table in the DB
       record_id: an integer representing an id of some record in the DB
    """
    if not isinstance(record_id, int):
        raise BadRequest('invalid id')
    return model.query.get_or_404(record_id,
                                  description="The requested record was not found")


def insert_into_db(model, new_record):
    """add the given record to the db

       record: it's a new record, an instance of some model
               (Department or Employee for example)
    """

    all_records = get_all(model)
    if len(all_records) == 0:
        new_record.id = 1
    else:
        new_record.id = all_records[-1].id + 1

    db.session.add(new_record)
    db.session.commit()


def delete_from_db(model, record):
    """delete the given record from the DB.

       record: it's a new record, an instance of some model
               (Department or Employee for example)
    """
    db.session.delete(record)

    records_after_deleted = model.query.filter(model.id > record.id).all()
    for rec in records_after_deleted:
        rec.id -= 1

    db.session.commit()


def update_department_name(dep, new_name):
    """update departement's name
       if department's name is not valid raise BadRequest(400) exception

       dep: the department to be updated
       new_name: the new_name to update with
    """
    if not Department.validate_name(new_name):
        raise BadRequest("Invalid department's name")

    if not new_name.endswith('department'):
        new_name += ' department'

    dep.name = new_name.strip()
    db.session.commit()


def update_employee(emp, fields: dict):
    """chech what fields are given and update them
       if not a single valid key was given then raise BadRequest

       fields: a dict with any of employee fields (fullname, bday, salary, department)
    """
    num_of_valid_keys = 4
    try:
        fullname = fields['fullname']
        if not Employee.validate_fullname(fullname):
            raise BadRequest("Invalid employee's name")
        emp.fullname = fullname
    except KeyError:
        num_of_valid_keys -= 1

    try:
        emp.bday = fields['bday']
    except KeyError:
        num_of_valid_keys -= 1

    try:
        salary = float(fields['salary'])
        emp.salary = salary
    except KeyError:
        num_of_valid_keys -= 1
    except ValueError:
        raise BadRequest('Salary must be numeric') from AttributeError

    try:
        # if the department does not exist than the dep is set to None
        # and since None does not have the id attribute AttributeError is raised
        dep = Department.query.filter_by(name=fields['dep_name']).first()
        emp.department_id = dep.id
    except KeyError:
        num_of_valid_keys -= 1
    except AttributeError:
        raise BadRequest("Uknown department name") from AttributeError

    if num_of_valid_keys == 0:
        raise BadRequest('provide some fields to update')

    try:
        db.session.commit()
    except Exception:
        raise ValueError(f"time data '{fields['bday']}' does not match format '%Y-%m-%d'")


def reload_db():
    """repopulate db before test to make sure that data is correct"""
    for emp, dep in zip(Employee.query.all(), Department.query.all()):
        db.session.delete(emp)
        db.session.delete(dep)

    db.session.commit()

    deps = [{'dep_name': 'Management department'},
            {'dep_name': 'Marketing department'},
            {'dep_name': 'Finance department'}]

    emps = [{
            'fullname': 'Sergey Monushko',
            'bday': date(1997, 10, 24),
            'salary': 463,
            'dep_name': 'Management department'
            },
            {
                'fullname': 'Victoria Nemko',
                'bday': date(1998, 8, 10),
                'salary': 553,
                'dep_name': 'MarketingManagement department'
            },
            {
                'fullname': 'Vladimir Severinec',
                'bday': date(1998, 8, 12),
                'salary': 534,
                'dep_name': 'Finance department'
            }]

    for emp, dep in zip(emps, deps):
        requests.post('http://localhost:5000/api/departments/', data=dep)
        requests.post('http://localhost:5000/api/employees', data=emp)
