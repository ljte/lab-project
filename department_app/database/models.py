import os

from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(64), nullable=False)
    second_name = Column(String(64), nullable=False)
    bday = Column(DateTime, nullable=False)
    
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="employees")

    @property
    def fullname(self):
        return " ".join([self.first_name, self.second_name])

    def __repr__(self):
        return f"{self.__class__.__name__}({self.fullname}, {self.bday})"


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False, unique=True)

    employees = relationship("Employee", order_by=Employee.id, back_populates="department")
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

