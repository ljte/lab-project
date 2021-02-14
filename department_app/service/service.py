from typing import Union, List, Mapping, Any

from loguru import logger

from department_app.domain.interfaces import IDatabase
from department_app.database import Base


class DatabaseService:

    def __init__(self, database: IDatabase):
        self.db = database

    def all(self, model: Base):
        with self.db.session() as s:
            try:
                records = s.query(model).all()
            except Exception as e:
                logger.exception(e)
                s.rollback()
            else:
                return records

    def get(self, model: Base, **criterion: Mapping[str, Any]):
        with self.db.session() as s:
            try:
                record = s.query(model).filter_by(**criterion).first()
            except Exception as e:
                logger.exception(e)
                s.rollback()
            else:
                return record