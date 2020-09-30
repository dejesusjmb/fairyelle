import uuid

from src.common.database import Database
import src.models.customers.constants as CustomerConstants


class Customer(object):
    def __init__(self, name, contact_number, address, landmarks=None, _id=None):
        self.name = name
        self.contact_number = contact_number
        self.address = address
        self.landmarks = landmarks
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.update(CustomerConstants.COLLECTION, {'_id': self._id}, self.json())

    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'contact_number': self.contact_number,
            'address': self.address,
            'landmarks': self.landmarks
        }

    @classmethod
    def find_by_id(cls, item_id):
        return cls(**Database.find_one(CustomerConstants.COLLECTION, {'_id': item_id}))
