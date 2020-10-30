"""interaction with databases"""

from datetime import datetime, date

from flask import abort

from department_app.models import db
from department_app.models.department import Department
from department_app.models.employee import Employee


def get_all(model):
    """return all the record in the
       table represented by model
       if the model does not exist
       raise ValueError if the table
       is empty return empty list []

       model: is a model of some table in the db
    """
    try:
        return model.query.all()
    except Exception:
        raise ValueError(f'given Model "{model}" is invalid') from None


def get_or_404(model, **criterion):
    """get the record from the model
       based on the given criterion
       if the record or the given
       criterion is invalid raise NotFound
       exception, the same happens when
       the invalid model is given

       model: is a model of some table in the db
       criterion: is a criterion on the function will filter
                  the result (e.g id=1 or name="Management department")
       """
    error_descr = f"The {model.__name__} with {criterion} was not found"
    return model.query.filter_by(**criterion).first_or_404(description=error_descr)


def insert_into_db(record):
    """insert record into the database, if record already exists
       return BadRequest, if record is invalid raise BadRequest

       record: is an object of the model class
    """
    if not isinstance(record, db.Model):
        abort(400)

    try:
        db.session.add(record)
        db.session.commit()
    except Exception:
        db.session.rollback()
        abort(500, f'Failed to insert {record}')


def delete_from_db(record):
    """delete record from the database,
       if record is invalid raise BadRequest

       record: is an object of the model class
    """
    if not isinstance(record, db.Model):
        abort(400, f'ivalid record {record}')

    try:
        db.session.delete(record)
        db.session.commit()
    except Exception:
        db.session.rollback()
        abort(500, f'can not delete record {record}')


def update_record(model, record, **new_fields):
    """update the record's fields

       model: is a model of some table in the db
       record: a record to update
       new_fields: fields to update with
    """
    if not isinstance(record, model):
        abort(400, f'invalid record {record}')

    if new_fields:
        try:
            # doing it just because sqlite test does not work otherwise
            try:
                new_fields['bday'] = datetime.strptime(str(new_fields['bday']), '%Y-%m-%d').date()
            except KeyError:
                pass
            model.query.filter_by(id=record.id).update(new_fields)
            db.session.commit()
        except Exception:
            db.session.rollback()
            abort(400, f"Failed to update {record}")
    else:
        abort(400, 'no fields to update were given')


def search_department_by_name(search_name: str):
    """find all the department which names resemble to the given name

    search_name: template name to search with
    """
    return Department.query.filter(Department.name.like(f'%{str(search_name).lower().title()}%')).all()


def search_employees_by_fullname(search_name: str):
    """find all the employees with fullname = search_name

    search_name: template name to search with
    """
    return Employee.query.filter(Employee.fullname.like(f'%{str(search_name).lower().title()}%')).all()


def filter_employees_by_bday(bday: date):
    """return employees with the birthday of bday
    """
    if not isinstance(bday, date):
        raise ValueError('invalid date format')
    return Employee.query.filter(Employee.bday == bday).all()


def filter_employees_by_date_period(start_date: date, end_date: date):
    """return employees with the birthday inside the period from start_date to end_date
    """
    if not isinstance(start_date, date) or not isinstance(end_date, date):
        raise ValueError('invalid date format')
    emps = Employee.query.filter(Employee.bday >= start_date).all()
    return [emp for emp in emps if emp.bday <= end_date]


def init_db_for_test():
    """populate db with test data"""
    deps = [Department(name='Finance department'),
            Department(name='Human Resource department'),
            Department(name='Accounting department'),
            Department(name='Sales department'),
            Department(name='Management department'),
            Department(name='Marketing department'),
            Department(name='Delete department'),
            Department(name='Edit department')]
    db.session.add_all(deps)
    db.session.commit()

    emps = [Employee(fullname='One Employee', salary=123, bday=date(1995, 12, 12), department_id=deps[0].id),
            Employee(fullname='Two Employee', salary=700, bday=date(1995, 12, 12), department_id=deps[2].id),
            Employee(fullname='Three Employee', salary=123, bday=date(1995, 12, 12), department_id=deps[1].id),
            Employee(fullname='Andrey Bobrov', salary=644, bday=date(1992, 6, 23), department_id=deps[3].id),
            Employee(fullname='Anna Volkova', salary=533, bday=date(1998, 10, 20), department_id=deps[4].id),
            Employee(fullname='Boris Nemchenko', salary=512, bday=date(1993, 6, 15), department_id=deps[5].id),
            Employee(fullname='Vladimir Novikov', salary=832, bday=date(1985, 9, 15), department_id=deps[5].id),
            Employee(fullname='Edit Employee', salary=1212, bday=date(1997, 12, 15), department_id=deps[4].id)]
    db.session.add_all(emps)
    db.session.commit()
