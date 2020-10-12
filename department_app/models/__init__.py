from department_app import db


class Department(db.Model):
    """A model for the table department.
        Each department has its unique id and name.
        For example Department(name='Sales department')
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

    def __repr__(self):
        return f"Deparment({self.name})"


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
        return f"Employee({self.fullname}, {self.bday}, {self.salary}, {self.department.name})"
