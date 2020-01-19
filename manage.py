from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand, upgrade
from acrobot.app import create_app

app, db = create_app()
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


def run_upgrade():
    """
    Execute migration plan
    """
    with app.app_context():
        upgrade()


if __name__ == '__main__':
    manager.run()
