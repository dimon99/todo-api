from flask_script import Manager
from flask_migrate import MigrateCommand
import app
from werkzeug.security import generate_password_hash,check_password_hash


manager = Manager(app.create_app())
manager.add_command( 'db', MigrateCommand )

@manager.command
def create_record():
    from models import Todo_list
    u = Todo_list(id='1', description="Fix my code_1", title="very importent_1", uri="d2dd", status="done_1")
    app.db.session.add(u)
    app.db.session.commit()
@manager.command
def create_user():
    from models import User
    pwd = generate_password_hash('dimon',method='pbkdf2:sha1',salt_length=8)
    user = User(username='dimon', password=pwd)
    app.db.session.add(user)
    app.db.session.commit()

if __name__ == "__main__":
    manager.run()