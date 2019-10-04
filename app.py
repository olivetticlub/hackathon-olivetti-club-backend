from flask import Flask, render_template, escape, request
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

class Merchant(db.Entity):
    name = Required(str, unique=True)

    def as_json(self):
        return { 'name': self.name }

db.bind(**app.config['PONY'])
db.generate_mapping(create_tables=True)

Pony(app)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/merchants', methods = ['POST'])
def create_merchant():
    merchant = db.Merchant(name=request.json['name'])
    return merchant.as_json()

