import uuid
from datetime import datetime

from src.common.database import Database
from src.models.items.item import Item
import src.models.orders.constants as OrderConstants


class Order(object):
    def __init__(self, customer_id, items, total_price,
                 notes=None, status='open', ordered_at=datetime.now(), _id=None):
        self.customer_id = customer_id
        self.items = items
        self.total_price = total_price
        self.notes = notes
        self.status = status
        self.ordered_at = ordered_at
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.update(OrderConstants.COLLECTION, {'_id': self._id}, self.json())

    def json(self):
        return {
            '_id': self._id,
            'customer_id': self.customer_id,
            'items': self.items,
            'ordered_at': self.ordered_at,
            'notes': self.notes,
            'status': self.status,
            'total_price': self.total_price
        }

    @classmethod
    def find_by_id(cls, order_id):
        return cls(**Database.find_one(OrderConstants.COLLECTION, {'_id': order_id}))

    def get_items(self):
        item_list = []

        for item_id, quantity in self.items.items():
            item = Item.find_by_id(item_id)
            item_details = item.json()
            item_details['quantity'] = quantity
            item_details['subtotal'] = quantity * item.price
            item_list.append(item_details)

        return item_list


    # def load_items(self, items):
    #     item_list = []
    #     total = 0
    #
    #     for item_id, quantity in items.items():
    #         item = Item.find_by_id(item_id)
    #         item_details = item.json()
    #         item_details['price'] = item.price
    #         item_details['subtotal'] = quantity * item.price
    #         items.append(item_details)
    #         total += item_details['subtotal']
    #