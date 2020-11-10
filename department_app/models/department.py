"""departments model"""

from sqlalchemy.sql import func

from department_app.models.employee import Employee
from department_app.models import db


class Department(db.Model):
    """A model for the table department.
        Each department has its unique id and name.
        For example Department(name='Sales department')
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

    def __repr__(self):
        return f"Department({self.name})"

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name

    def to_dict(self):
        """transform the department into a dictionary"""
        data = {
            'name': self.name,
            'id': self.id,
            'number_of_employees': self.number_of_employees(),
            'average_salary': self.average_salary()
        }
        return data

    def number_of_employees(self):
        """count the number of employees"""
        return Employee.query.with_entities(
                  func.count(Employee.id).label('num_of_emps')
               ).filter_by(department_id=self.id).first()[0]

    def average_salary(self):
        """count average salary"""
        try:
            average_salary = round(Employee.query.with_entities(
                                      func.avg(Employee.salary).label('avg_salary')
                                  ).filter_by(department_id=self.id).first()[0], 2)
        except TypeError:
            average_salary = 0
        return average_salary

    @classmethod
    def validate_name(cls, name):
        """check if the name is valid"""

        if not isinstance(name, str):
            return False

        # if name is empty or if it consists only of spaces return False
        if name == '' or name.isspace():
            return False

        # if the name has 'department' in it but it is not separated with space return False
        # for example Managementdepartment
        if "department" in name and len(name.split()) == 1:
            return False

        # if a number occurs in department's name return False
        for letter in name:
            if letter == " ":
                pass
            elif letter.isdigit():
                return False

        return True

    @classmethod
    def name_does_not_exist(cls, name: str):
        """check if department with the given name already exists"""
        # if the department already exists return False
        if 'department' not in name:
            name += ' department'
        return cls.query.filter_by(name=name).first() is None
