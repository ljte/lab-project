from datetime import date, datetime
from typing import Optional, Union

from django.shortcuts import get_object_or_404
from pydantic import BaseModel, validator

from ..models import Department, Employee
from .department_schema import DepartmentSchema
from .helpers import check_for_digits


class EmployeeSchema(BaseModel):
    id: Optional[int]
    first_name: str
    second_name: str
    salary: float
    bday: Union[str, date]
    department: Union[str, DepartmentSchema]

    @validator("first_name", "second_name")
    def fullname_is_valid(cls, v):
        if check_for_digits(v):
            raise ValueError("Invalid name `%s`" % v)
        return v.capitalize().strip()

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
    def jsonify(cls, emp):
        emp = cls.from_orm(emp).dict()
        return emp

    @classmethod
    def to_orm(cls, emp_dict):
        dep = Department.objects.filter(name=emp_dict["department"]).first()
        emp = cls.parse_obj(emp_dict).dict()
        emp.update({"department": dep})
        return Employee(**emp)

    @classmethod
    def parse_obj(cls, emp):
        emp = super().parse_obj(emp)
        if hasattr(emp, "id"):
            delattr(emp, "id")
        return emp

    @classmethod
    def from_put(cls, updated_fields):
        first_name = updated_fields.get("first_name")
        second_name = updated_fields.get("second_name")
        dep = updated_fields.get("department")
        if first_name:
            cls.fullname_is_valid(first_name)
        if second_name:
            cls.fullname_is_valid(second_name)
        if dep:
            updated_fields.update(
                {"department": get_object_or_404(Department, name=dep)}
            )
        return {k: v for k, v in updated_fields.items() if v is not None}

    class Config:
        orm_mode = True
