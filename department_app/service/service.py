from typing import Union, List, Mapping, Any

from loguru import logger
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from department_app.domain.interfaces import IDatabase
from department_app.domain.exceptions import RecordAlreadyExistsError
from department_app.database import Base


class DatabaseService:

    def __init__(self, database: IDatabase):
        self.db = database

    def all(self, model: Base) -> List[Base]:
        with self.db.session() as s:
            try:
                records = s.query(model).all()
            except SQLAlchemyError:
                s.rollback()
                raise
            return records

    def get(self, model: Base, **criterion: Mapping[str, Any]) -> Base:
        with self.db.session() as s:
            try:
                record = s.query(model).filter_by(**criterion).first()
            except SQLAlchemyError:
                s.rollback()
                raise
            return record or None

    def insert(self, record: Base) -> None:
        with self.db.session() as s :
            try:
                s.add(record)
                s.commit()
            except IntegrityError as e:
                raise RecordAlreadyExistsError(record) from e
            except SQLAlchemyError:
                raise
            finally:
                s.rollback()

    def update(self, record: Base, **updated_fieds: Mapping[str, Any]) -> None:
        with self.db.session() as s:
            try:
                s.query(type(record)).\
                        filter_by(id = record.id).\
                        update(updated_fieds)
                s.commit()
            except SQLAlchemyError:
                s.rollback()
                raise

    def delete(self, record: Base) -> None:
        with self.db.session() as s:
            try:
                s.delete(record)
                s.commit()
            except SQLAlchemyError:
                s.rollback()
                raise
