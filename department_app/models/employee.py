"""employees model"""

from department_app.models import db


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
            'department': self.department.name
        }
        return data

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
