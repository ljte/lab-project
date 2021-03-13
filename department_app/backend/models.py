from django.db import models
from django.db.models import Avg

from .service import get_obj


class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)

    @property
    def number_of_employees(self):
        return self.employees.count()

    @property
    def average_salary(self):
        query = self.employees.aggregate(average_salary=Avg("salary"))
        return query.get("average_salary") or 0

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"


class Employee(models.Model):
    fullname = models.CharField(max_length=256)
    bday = models.DateField()
    salary = models.FloatField()
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="employees",
    )

    def __str__(self):
        return self.fullname

    def __repr__(self):
        return f"{self.__class__.__name__}({self.fullname}, {self.bday}, {self.salary}, {self.department.name})"

    @classmethod
    def from_dict(cls, d):
        d.update({"department": get_obj(Department, name=d["department"])})
        return cls(**d)
