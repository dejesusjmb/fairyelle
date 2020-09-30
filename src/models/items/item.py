import uuid

from src.common.database import Database
import src.models.items.constants as ItemConstants


class Item(object):
    def __init__(self, name, price, category, subcategory, description, image_url, _id=None):
        self.name = name
        self.price = price
        self.description = description
        self.image_url = image_url
        self.category = category
        self.subcategory = subcategory
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.update(ItemConstants.COLLECTION, {'_id': self._id}, self.json())

    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'price': self.price,
            'image_url': self.image_url,
            'description': self.description,
            'category': self.category,
            'subcategory': self.subcategory
        }

    @classmethod
    def find_by_id(cls, item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {'_id': item_id}))

    @staticmethod
    def find_by_category(category):
        return [Item(**item) for item in Database.find(ItemConstants.COLLECTION,
                                                       {'category': category})]

    def delete(self):
        Database.remove(ItemConstants.COLLECTION, {'_id': self._id})
