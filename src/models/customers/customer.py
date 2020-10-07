import uuid
from datetime import datetime

from src.common.database import Database
import src.models.customers.constants as CustomerConstants


class Customer(object):
    def __init__(self, name, contact_number, birthdate, address,
                 landmarks=None, ordered_at=None, _id=None):
        self.name = name
        self.contact_number = contact_number
        self.birthdate = birthdate
        self.address = address
        self.landmarks = landmarks
        self.ordered_at = ordered_at or datetime.now()
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.update(CustomerConstants.COLLECTION, {'_id': self._id}, self.json())

    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'contact_number': self.contact_number,
            'birthdate': self.birthdate,
            'address': self.address,
            'landmarks': self.landmarks,
            'ordered_at': self.ordered_at
        }

    @classmethod
    def find_by_id(cls, item_id):
        return cls(**Database.find_one(CustomerConstants.COLLECTION, {'_id': item_id}))

    def is_in_legal_age(self):
        return (datetime.now() - self.birthdate).days / 365 >= 21

    @classmethod
    def get_customers(cls, query=None):
        query = query or {}
        return [cls(**customer) for customer in Database.find(CustomerConstants.COLLECTION, query)]
