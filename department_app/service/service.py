from typing import Any, List

from sqlalchemy.exc import (IntegrityError, InvalidRequestError,
                            OperationalError)
from sqlalchemy.orm.exc import UnmappedInstanceError

from department_app.database import Base
from department_app.domain.exceptions import (InvalidModelError,
                                              InvalidRecordError,
                                              ModelNotFoundError,
                                              RecordAlreadyExistsError,
                                              RecordNotFoundError)
from department_app.domain.interfaces import IDatabase


class DatabaseService:
    def __init__(self, database: IDatabase):
        self.db = database

    def all(self, model: Base) -> List[Base]:
        with self.db.session() as s:
            try:
                records = s.query(model).all()
            except (OperationalError, InvalidRequestError) as e:
                s.rollback()
                raise ModelNotFoundError("Invalid model `%s`" % model) from e
            return records

    def get(self, model: Base, **criterion: Any) -> Base:
        with self.db.session() as s:
            try:
                record = s.query(model).filter_by(**criterion).first()
            except (OperationalError, InvalidRequestError) as e:
                s.rollback()
                raise InvalidModelError(
                    "Invalid model `%s` or fields %s" % (model, criterion)
                ) from e
            return record

    def insert(self, record: Base) -> None:
        with self.db.session() as s:
            try:
                s.add(record)
                s.commit()
            except IntegrityError as e:
                s.rollback()
                raise RecordAlreadyExistsError(record) from e

    def update(self, record: Base, **updated_fieds: Any) -> None:
        with self.db.session() as s:
            try:
                s.query(type(record)).filter_by(id=record.id).update(updated_fieds)
                s.commit()
            except IntegrityError as e:
                s.rollback()
                raise RecordNotFoundError(
                    "Department with id `%d` does not exist"
                    % updated_fieds["department_id"]
                ) from e
            except InvalidRequestError as e:
                s.rollback()
                raise InvalidRecordError(
                    "Invalid record `%s` or fields `%s`" % (record, updated_fieds)
                ) from e

    def delete(self, record: Base) -> None:
        with self.db.session() as s:
            try:
                s.delete(record)
                s.commit()
            except (UnmappedInstanceError, InvalidRequestError) as e:
                s.rollback()
                raise RecordNotFoundError("Invalid record `%s`" % s) from e
