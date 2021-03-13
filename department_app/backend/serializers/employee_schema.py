from datetime import date, datetime
from typing import Optional, Union

from pydantic import validator

from ..models import Department, Employee
from ..service import get_obj
from .department_schema import DepartmentSchema
from .generic_schema import ORMModel
from .helpers import check_for_digits


class EmployeeSchema(ORMModel):
    id: Optional[int]
    fullname: Optional[str]
    salary: Optional[float]
    bday: Optional[Union[str, date]]
    department: Optional[Union[str, DepartmentSchema]]

    @validator("fullname")
    def fullname_is_valid(cls, v):
        if check_for_digits(v):
            raise ValueError("Invalid name `%s`" % v)
        return v.title().strip()

    @validator("bday")
    def age_is_not_too_big(cls, v):
        if isinstance(v, str):
            v = datetime.strptime(v, "%Y-%m-%d").date()
        if datetime.utcnow().year - v.year > 100:
            raise ValueError("Age is to big %s" % v)
        return v

    @validator("department")
    def get_department_name(cls, v):
        if isinstance(v, DepartmentSchema):
            v = v.name
        return v

    @classmethod
    def dump_obj(cls, emp):
        return cls.from_orm(emp).dict()

    @classmethod
    def loads(cls, obj_dict):
        return super().loads(obj_dict, Employee)

    @classmethod
    def process(cls, obj_dict):
        obj = super().process(obj_dict)
        dep_name = obj["department"]
        if dep_name is not None:
            obj.update({"department": get_obj(Department, name=dep_name)})
        return obj
