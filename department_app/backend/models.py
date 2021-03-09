from django.db import models
from django.db.models import Avg


class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)

    @property
    def number_of_employees(self):
        return self.employees.count()  # type: ignore

    @property
    def average_salary(self):
        query = self.employees.aggregate(average_salary=Avg("salary"))  # type: ignore
        return query.get("average_salary") or 0

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"


class Employee(models.Model):
    first_name = models.CharField(max_length=128)
    second_name = models.CharField(max_length=128)
    bday = models.DateField()
    salary = models.FloatField()
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="employees",
    )

    @property
    def fullname(self):
        return " ".join((self.first_name, self.second_name))  # type: ignore

    def __str__(self):
        return self.fullname

    def __repr__(self):
        return f"{self.__class__.__name__}({self.fullname}, {self.bday}, {self.department.name})"
