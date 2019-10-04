from flask import Flask, render_template, escape, request
from flask_login import LoginManager, UserMixin, login_required
from pony.flask import Pony
from pony.orm import Database, Required, Optional
from datetime import datetime

app = Flask(__name__)
app.config.update(dict(
    DEBUG = False,
    SECRET_KEY = 'secret_xxx',
    PONY = {
        'provider': 'sqlite',
        'filename': 'db.db3',
        'create_db': True
    }
))

db = Database()

class User(db.Entity, UserMixin):
    login = Required(str, unique=True)
    password = Required(str)
    last_login = Optional(datetime)

db.bind(**app.config['PONY'])
db.generate_mapping(create_tables=True)

Pony(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.User.get(id=user_id)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

