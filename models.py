from pony.flask import Pony
from pony.orm import Database, Required, Optional, PrimaryKey, Set, select

db = Database()

class Merchant(db.Entity):
    name = Required(str, unique=True)
    vat_number = Required(str, unique=True)
    ateco = Required(str)
    address = Optional(str)
    latitude = Optional(float)
    longitude = Optional(float)
    deals = Set('Deal')
    consumed_coupons = Set('Coupon')

    def before_insert(self):
        location = geocoder.komoot(self.address)
        self.latitude = location.lat
        self.longitude = location.lng

    def coordinates(self):
        return dict(lat=self.latitude, lng=self.longitude)

    def as_json(self):
        deals = [deal.as_json() for deal in self.deals]
        return {
                'name': self.name,
                'vat_number': self.vat_number,
                'ateco': self.ateco,
                'address': self.address,
                'coordinates': self.coordinates(),
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
