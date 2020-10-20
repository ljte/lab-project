"""application initialization"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api

from department_app.config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


from department_app.models.department import Department
from department_app.models.employee import Employee
from department_app.rest.department_api import DepartmentApi
from department_app.rest.employee_api import EmployeeApi


api = Api(app)
api.add_resource(DepartmentApi, *DepartmentApi.urls)
api.add_resource(EmployeeApi, *EmployeeApi.urls)
