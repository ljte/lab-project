from datetime import datetime, date
from typing import Optional, Union

from pydantic import BaseModel, validator

from .helpers import check_for_digits


class DepartmentSchema(BaseModel):
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

    class Config:
        orm_mode = True


class DepartmentSchemaDB(DepartmentSchema):
    id: int
    avg_salary: float
    num_of_employees: int


class EmployeeSchema(BaseModel):
    first_name: Optional[str]
    second_name: Optional[str]
    bday: Optional[Union[date, str]]
    salary: Optional[float]
    department_id: Optional[int]

    @validator("first_name", "second_name")
    def fullname_is_valid(cls, v: str):
        if check_for_digits(v):
            raise ValueError("Invalid name `%s`" % v)
        return v.capitalize().strip()

    @validator("bday")
    def age_is_not_too_big(cls, v: Union[str, date]):
        if isinstance(v, str):
            v = datetime.strptime(v, "%Y-%m-%d").date()
        if datetime.utcnow().year - v.year > 100:
            raise ValueError("Age is to big %s" % v)
        return v

    class Config:
        orm_mode = True


class EmployeeSchemaDB(EmployeeSchema):
    id: int
