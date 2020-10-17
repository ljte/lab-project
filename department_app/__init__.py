from configparser import ConfigParser

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api


config = ConfigParser()
config.read('./config.ini')

# create app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config['database']['uri']
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = bool(config['sqlalchemy']['track_modifications'])

db = SQLAlchemy(app)
migrate = Migrate(app, db, directory=config['sqlalchemy']['migrations_dir'])
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# avoid cyclic imports
from department_app.models import Department, Employee
from department_app.rest import DepartmentApi, EmployeeApi

# add rest resources
api = Api(app)
api.add_resource(DepartmentApi, *DepartmentApi.urls)
api.add_resource(EmployeeApi, *EmployeeApi.urls)
