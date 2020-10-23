"""interaction with databases"""

from datetime import datetime

from flask import abort

from department_app.models import db


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
