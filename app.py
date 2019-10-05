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
    vat_number = Required(str, unique=True)
    ateco = Required(str)
    address = Optional(str)
    deals = Set('Deal')
    consumed_coupons = Set('Coupon')

    def as_json(self):
        deals = [deal.as_json() for deal in self.deals]
        return {
                'name': self.name,
                'vat_number': self.vat_number,
                'ateco': self.ateco,
                'address': self.address,
                'deals': deals
                }

class Deal(db.Entity):
    id = PrimaryKey(int, auto=True)
    coupons = Set('Coupon')
    merchant = Required(Merchant)
    description = Required(str)

    def generated_coupons_count(self):
        return len(self.coupons)

    def consumed_coupons_count(self):
        return len([coupon for coupon in self.coupons if coupon.consumed()])

    def generate_coupons(self, count):
        for i in range(count):
            db.Coupon(deal=self)

    def as_json(self):
        json = { 'id': self.id,
                'merchant': self.merchant.name,
                'description': self.description,
                'generated_coupons_count': self.generated_coupons_count(),
                'consumed_coupons_count': self.consumed_coupons_count()
                }
        return json

class Coupon(db.Entity):
    id = PrimaryKey(int, auto=True)
    deal = Required(Deal)
    consumed_at = Optional(Merchant)

    def consumed(self):
        return self.consumed_at is not None

    def valid(self):
        return not self.consumed()

    def as_json(self):
        return { 'id': self.id,
                'deal': {
                    'id': self.deal.id,
                    'description': self.deal.description,
                    },
                'consumed_at': self.consumed_at.name
                }

db.bind(**app.config['PONY'])
db.generate_mapping(create_tables=True)

Pony(app)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/merchants', methods = ['POST'])
def create_merchant():
    merchant_data = request.json
    merchant = db.Merchant(**merchant_data)
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
    deal = db.Deal(merchant=merchant, description=coupon_data['description'])
    deal.generate_coupons(count)

    return deal.as_json()

@app.route('/coupons/consume', methods = ['POST'])
def consume_coupon():
    coupon = select(coupon for coupon in Coupon if coupon.valid()).random(1)[0]
    merchant = db.Merchant.get(name=request.json['merchant'])
    coupon.consumed_at = merchant

    return coupon.as_json()

