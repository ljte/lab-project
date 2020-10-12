from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from configparser import ConfigParser


config = ConfigParser()
config.read('../config.ini')

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config['database']['uri']
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = bool(config['sqlalchemy']['track_modifications'])

db = SQLAlchemy(app)
migrate = Migrate(app, db, directory=config['sqlalchemy']['migrations_dir'])
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from department_app.models import Department, Employee
