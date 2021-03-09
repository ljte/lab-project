from typing import Optional

from pydantic import BaseModel, validator

from ..models import Department
from .helpers import check_for_digits


class DepartmentSchema(BaseModel):
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
    def jsonify(cls, dep):
        d = cls.from_orm(dep)
        return {
            "id": d.id,
            "name": d.name,
            "number_of_employees": dep.number_of_employees,
            "average_salary": dep.average_salary,
        }

    @classmethod
    def to_orm(cls, dep):
        d = cls.parse_obj(dep)
        return Department.from_dict(d)

    @classmethod
    def parse_obj(cls, dep):
        d = super().parse_obj(dep).dict()
        del d["id"]
        return d

    class Config:
        orm_mode = True
