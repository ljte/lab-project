from sqlalchemy import Column, Date, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Employee(Base):  # type: ignore
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(64), nullable=False)
    second_name = Column(String(64), nullable=False)
    salary = Column(Float, nullable=False)
    bday = Column(Date, nullable=False)

    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="employees", lazy='joined')

    @property
    def fullname(self):
        return " ".join([self.first_name, self.second_name])

    def __repr__(self):
        return f"{self.__class__.__name__}({self.fullname}, {self.bday})"

    def __eq__(self, other):
        return self.name == other.name


class Department(Base):  # type: ignore
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False, unique=True)

    employees = relationship(
        "Employee", order_by=Employee.id, back_populates="department", lazy='joined'
    )

    @property
    def avg_salary(self):
        emps_len = len(self.employees)
        return sum([emp.salary for emp in self.employees]) / emps_len if emps_len > 0 else 0

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"
