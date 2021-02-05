from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    
    employees = db.relationship("Employee", backref="department", lazy=True)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id}, {self.name})"


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)

    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id}, {self.name} {self.surname}, {self.birthday})"