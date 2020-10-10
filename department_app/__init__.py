from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://user_1:12345@localhost:5432/test"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db, directory='department_app/migrations')
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from department_app.models import Department, Employee

