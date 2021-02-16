from typing import Any, List, Mapping

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
                raise ModelNotFoundError("Invalid model `%s`" % model) from e
            finally:
                s.rollback()
            return records

    def get(self, model: Base, **criterion: Mapping[str, Any]) -> Base:
        with self.db.session() as s:
            try:
                record = s.query(model).filter_by(**criterion).first()
            except (OperationalError, InvalidRequestError) as e:
                raise InvalidModelError(
                    "Invalid model `%s` or fields %s" % (model, criterion)
                ) from e
            return record or None

    def insert(self, record: Base) -> None:
        with self.db.session() as s:
            try:
                s.add(record)
                s.commit()
            except IntegrityError as e:
                raise RecordAlreadyExistsError(record) from e
            finally:
                s.rollback()

    def update(self, record: Base, **updated_fieds: Mapping[str, Any]) -> None:
        with self.db.session() as s:
            try:
                s.query(type(record)).filter_by(id=record.id).update(updated_fieds)
                s.commit()
            except InvalidRequestError as e:
                raise InvalidRecordError(
                    "Invalid record `%s` or fields `%s`" % (record, updated_fieds)
                ) from e
            finally:
                s.rollback()

    def delete(self, record: Base) -> None:
        with self.db.session() as s:
            try:
                s.delete(record)
                s.commit()
            except (UnmappedInstanceError, InvalidRequestError) as e:
                raise RecordNotFoundError("Invalid record `%s`" % s) from e
            finally:
                s.rollback()
