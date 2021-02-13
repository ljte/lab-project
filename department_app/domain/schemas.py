from datetime import datetime
from string import digits

from pydantic import BaseModel, validator

from .helpers import check_for_digits


class DepartmentSchema(BaseModel):
    id: int
    name: str

    @validator("name")
    def validate_name(cls, v: str):
        # validate that name does not include digits
        if check_for_digits(v):
            raise ValueError("Invalid department's name `%s`" % v)

        # remove redundant whitespaces
        v = " ".join([word.strip() for word in v.split()])

        # add `department` to the name if it is not there
        if not v.endswith("department"):
            v = " ".join([v, "department"])
        return v.capitalize().strip()


class EmployeeSchema(BaseModel):
    id: int
    first_name: str
    second_name: str
    bday: datetime
    department_id: int

    @validator("first_name", "second_name")
    def fullname_is_valid(cls, v: str):
        if check_for_digits(v):
            raise ValueError("Invalid name `%s`" % v)
        return v.capitalize().strip()

    @validator("bday")
    def age_is_not_too_big(cls, v: datetime):
        if datetime.utcnow().year - v.year > 100:
            raise ValueError("Age is to big %s" % v)
        return v