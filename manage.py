# coding:utf-8
from ihome import create_app, db
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand


app = create_app("develop")

manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(use_debugger=True, host='0.0.0.0'))


if __name__ == '__main__':
    manager.run()
