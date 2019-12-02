import requests
from pony.orm import select
from models import Merchant, Coupon

AI_URL = 'https://70f4680b.ngrok.io/merchants'

def best_coupon(merchant):
    all_merchants_with_coupons_but_me = [
            m.as_json()
            for m in select(m for m in Merchant if m.name != merchant.name)
            if m.has_running_deals()
            ]
    request_body = dict(
            referringMerchant=merchant.as_json(),
            merchantsPool=all_merchants_with_coupons_but_me)

    merchants = requests.post(AI_URL, json=request_body).json()
    merchants_name = [ merchant['owner'] for merchant in merchants ]
    coupons = select(
            coupon for coupon in Coupon
            if coupon.valid() and coupon.deal.merchant.name in merchants_name
            ).random(1)

    if not coupons:
        return None
    return coupons[0]
