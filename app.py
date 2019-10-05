from flask import Flask, render_template, escape, request
from pony.flask import Pony
from pony.orm import Database, Required, Optional, PrimaryKey, Set, select
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
    coupons = Set('Coupon', reverse='merchant')
    consumed_coupons = Set('Coupon', reverse='consumed_at')

    def as_json(self):
        coupons = [coupon.as_json() for coupon in self.coupons]
        return { 'name': self.name, 'coupons': coupons }

class Coupon(db.Entity):
    id = PrimaryKey(int, auto=True)
    merchant = Required(Merchant)
    description = Required(str)
    consumed_at = Optional(Merchant)

    def consumed(self):
        return self.consumed_at is not None

    def valid(self):
        return not self.consumed()

    def as_json(self):
        json = { 'id': self.id,
                'valid': self.valid(),
                'consumed_at': self.consumed_at.name if self.consumed_at else None,
                'merchant': self.merchant.name,
                'description': self.description }
        return json

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

@app.route('/merchants/<name>')
def show_merchant(name):
    merchant = db.Merchant.get(name=name)
    return merchant.as_json()

@app.route('/coupons', methods = ['POST'])
def create_coupons():
    coupon_data = request.json

    count = int(coupon_data['count'])
    merchant = db.Merchant.get(name=coupon_data['merchant'])
    for i in range(count):
        db.Coupon(merchant=merchant, description=coupon_data['description'])

    return coupon_data

@app.route('/coupons/consume', methods = ['POST'])
def consume_coupon():
    coupon = select(coupon for coupon in Coupon if coupon.valid()).random(1)[0]
    merchant = db.Merchant.get(name=request.json['merchant'])
    coupon.consumed_at = merchant

    return coupon.as_json()

