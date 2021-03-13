from typing import Optional

from pydantic import validator

from ..models import Department
from .generic_schema import ORMModel
from .helpers import check_for_digits


class DepartmentSchema(ORMModel):
    id: Optional[int]
    name: str

    @validator("name")
    def validate_name(cls, v):
        if check_for_digits(v):
            raise ValueError("Invalid department's name `%s`" % v)

        v = " ".join([word.strip() for word in v.split()])

        if not v.endswith("department"):
            v = " ".join([v, "department"])
        return v.capitalize().strip()

    @classmethod
    def dump_obj(cls, dep):
        # get Department object and create a dict from it
        dep_dict = cls.from_orm(dep).dict()
        dep_dict.update(
            {
                "number_of_employees": dep.number_of_employees,
                "average_salary": dep.average_salary,
            }
        )
        return dep_dict

    @classmethod
    def loads(cls, dep_dict):
        return super().loads(dep_dict, Department)
