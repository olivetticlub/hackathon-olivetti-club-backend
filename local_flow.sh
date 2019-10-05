#!/bin/bash

echo "+++ Creating merchant"
curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/merchants --data '{"name": "danielefongo", "vat_number": "12345", "ateco": "01.11.10", "address": "Somewhere in Umbria"}'

echo "+++ Creating coupons"
curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/coupons --data '{"merchant": "danielefongo", "description": "Buy one beer, get another for free","count":2}'

echo "+++ Retrieving merchant info"
curl http://localhost:5000/merchants/danielefongo

echo "+++ Consuming a coupon"
curl -X POST -H 'Content-Type: application/json' -i http://localhost:5000/coupons/consume --data '{"merchant": "danielefongo"}'

