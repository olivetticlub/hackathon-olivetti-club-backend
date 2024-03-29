from flask import Flask, render_template, escape, request
from flask_cors import CORS
from pony.orm import commit, delete
from models import *
from ai_utils import best_coupon
import random

app = Flask(__name__)
CORS(app)

app.config.update(dict(
    DEBUG = False,
    SECRET_KEY = 'secret_xxx',
    PONY = {
        'provider': 'sqlite',
        'filename': 'db.db3',
        'create_db': True
    },
    AI_ENABLED = False,
))

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
    commit()

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
    commit()

    return deal.as_json()

def _most_suitable_coupon(merchant):
    if app.config['AI_ENABLED']:
        return best_coupon(merchant)

    coupons = select(
            coupon for coupon in Coupon
            if coupon.valid() and coupon.deal.merchant.name != merchant.name
            ).random(1)

    return coupons[0] if coupons else None

def add_demo_merchant():
    merchant = db.Merchant(name="demo-merchant", vat_number=str(random.randint(0,1000)), ateco = "585858" )
    commit()
    return merchant

@app.route('/coupons/consume', methods = ['POST'])
def consume_coupon():
    merchant = db.Merchant.get(name=request.json['merchant'])

    if merchant is None and request.json['merchant'] == "demo-merchant":
        merchant = add_demo_merchant()

    coupon = _most_suitable_coupon(merchant)
    if coupon is None:
        return { 'message': 'No coupon available' }

    coupon.consumed_at = merchant
    return coupon.as_json()

@app.route('/reset', methods = ['GET'])
def reset():
    delete(coupon for coupon in Coupon)
    delete(merchant for merchant in Merchant)
    delete(deal for deal in Deal)

    return { 'message': 'Deleted everything!' }


if __name__ == '__main__':
    app.run(port=5000)