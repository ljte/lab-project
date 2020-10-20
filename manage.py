from flask_script import Manager
from flask_migrate import MigrateCommand

from department_app import create_app


if __name__ == "__main__":
    manager = Manager(create_app())
    manager.add_option("-c", "--config", dest="config_module", required=False)
    manager.add_command('db', MigrateCommand)
    manager.run()
