"""database models"""

from sqlalchemy.sql import func

from department_app import db


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
        return self.id == other.id

    def to_dict(self):
        """transform the department into a dictionary"""
        data = {
            'id': self.id,
            'name': self.name,
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
        return Employee.query.with_entities(
                    func.avg(Employee.salary).label('avg_salary')
                    ).filter_by(department_id=self.id).first()[0]

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

        # if the department already exists return False
        if 'department' not in name:
            name += ' department'
        return cls.query.filter_by(name=name).first() is None


class Employee(db.Model):
    """A model for the table employee.
       Each employee has its unique id, fullname, birthdate, salary
       and the id of the department that he works in.
       For example Employee(fullname='Andrey Semenov',
                            bday=date(1995, 10, 12),
                            salary=412.23,
                            department_id=2)
    """
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(64), nullable=False)
    bday = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Float, nullable=False)

    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    department = db.relationship('Department',
                                 backref=db.backref('employees', lazy=True))

    def __repr__(self):
        return f"Employee({self.id}, {self.fullname}, {self.bday}, {self.salary}, {self.department_id})"

    def __eq__(self, other):
        return self.id == other.id

    def to_dict(self):
        """tranfrom an Employee to a dictionary"""
        data = {
            'id': self.id,
            'fullname': self.fullname,
            'bday': self.bday.strftime("%d-%m-%Y"),
            'salary': self.salary,
            'department': self.department_name()
        }
        return data

    def department_name(self):
        """get the name of the department"""
        try:
            dep_name = self.department.name
        except AttributeError:
            dep_name = None
        return dep_name

    @staticmethod
    def validate_fullname(fullname):
        """make sure that the given name is
           actually something that looks like a name
        """
        # chech if the fullname is not empty or just spaces
        if fullname == '' or fullname.isspace():
            return False

        # fullname must consist of first and second names
        if len(fullname.split()) < 2:
            return False

        for letter in fullname:
            if letter == ' ':
                pass
            if letter.isdigit():
                return False

        return True
