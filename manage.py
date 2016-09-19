from flask_script import Manager, Shell
from app import create_app, db
from app.models import Article, Category, Price, Commodity
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS

app = create_app()
CORS(app)
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Article=Article, Category=Category, Price=Price, Commodity=Commodity)


manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=make_shell_context))

manager.add_command('runserver', app.run(host='0.0.0.0', port=8000))

if __name__ == '__main__':
    manager.run()
