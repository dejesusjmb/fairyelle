import uuid
from datetime import datetime

import requests

from src.common.database import Database
from src.models.customers.customer import Customer
from src.models.items.item import Item
import src.models.orders.constants as OrderConstants


class Order(object):
    def __init__(self, customer_id, items, total_price, delivery,
                 notes=None, status='open', ordered_at=datetime.now(), _id=None):
        self.customer_id = customer_id
        self.items = items
        self.total_price = total_price
        self.delivery = delivery
        self.notes = notes
        self.status = status
        self.ordered_at = ordered_at
        self._id = (datetime.now().strftime("%Y%m%d%H%M%S") + uuid.uuid4().hex[:4]
                    if _id is None else _id)
        self.summary = self.get_summary()

    def save_to_mongo(self):
        Database.update(OrderConstants.COLLECTION, {'_id': self._id}, self.json())

    def json(self):
        return {
            '_id': self._id,
            'customer_id': self.customer_id,
            'items': self.items,
            'delivery': self.delivery,
            'ordered_at': self.ordered_at,
            'notes': self.notes,
            'status': self.status,
            'total_price': self.total_price
        }

    @classmethod
    def find_by_id(cls, order_id):
        return cls(**Database.find_one(OrderConstants.COLLECTION, {'_id': order_id}))

    def get_summary(self):
        customer = Customer.find_by_id(self.customer_id).json()
        item_list = []
        for item_id, quantity in self.items.items():
            item = Item.find_by_id(item_id)
            item_details = {
                'name': item.name,
                'price': item.price,
                'subcategory': item.subcategory,
                'quantity': quantity,
                'subtotal': quantity * item.price
            }
            item_list.append(item_details)

        order_summary = {
            'order_id': self._id,
            'customer_name': customer['name'],
            'customer_contact_number': customer['contact_number'],
            'customer_address': customer['address'],
            'customer_landmarks': customer['landmarks'],
            'order_notes': self.notes,
            'order_delivery': self.delivery,
            'order_total_price': self.total_price,
            'order_ordered_at': self.ordered_at,
            'items': item_list,
            'order_status': self.status
        }

        return order_summary

    def send_notification(self):
        summary = self.summary
        items = summary.pop('items')

        rows = ('<tr><td style="width: 180px;"><strong>Order Id</strong></td>'
                '<td style="width: 372px;">'
                '<a href="http://127.0.0.1:4990/orders/acknowledge?order_id={order_id}">{order_id}'
                '</a></td></tr>').format(order_id=self._id)
        row = ('<tr><td style="width: 180px;"><strong>{key}</strong></td>'
               '<td style="width: 372px;">{value}</td></tr>')
        fields = ['customer_name', 'customer_contact_number', 'customer_address',
                  'customer_landmarks', 'order_delivery', 'order_notes', 'order_ordered_at',
                  'order_total_price']

        for field in fields:
            key = ' '.join(field.split('_')[1:]).title()
            rows += row.format(key=key, value=summary[field])

        order_table = '<table style="width: 568px;"><tbody>{rows}</tbody></table>'.format(rows=rows)

        item_rows = ('<tr><td style="width: 475px;"><strong>Subcategory</strong></td>'
                     '<td style="width: 562px;"><strong>Name</strong></td>'
                     '<td style="width: 23px;"><strong>#</strong></td>'
                     '<td style="width: 98px; text-align: right;"><strong>Price</strong></td>'
                     '<td style="width: 98px; text-align: right;"><strong>Subtotal</strong></td></tr>')
        item_row = ('<tr><td style="width: 475px;">{subcategory}</td>'
                    '<td style="width: 562px;">{name}</td>'
                    '<td style="width: 23px;">{quantity}</td>'
                    '<td style="width: 98px; text-align: right;">{price}</td>'
                    '<td style="width: 98px; text-align: right;">{subtotal}</td></tr>')

        for item in items:
            item_rows += item_row.format(**item)

        items_table = ('<table style="width: 568px;"><tbody>'
                       '{rows}</tbody></table>').format(rows=item_rows)

        message = order_table + '<p>&nbsp;</p><hr /><p>&nbsp;</p>' + items_table

        requests.post(
            "https://api.mailgun.net/v3/sandbox5593ce651a4c452bb25f4ef1512c934b.mailgun.org/messages",
            auth=("api", "key-b41cc766321f03b2c117b8eaa910016b"),
            data={
                "from": "New Order <mailgun@sandbox5593ce651a4c452bb25f4ef1512c934b.mailgun.org>",
                "to": ["vapersworldph@gmail.com"],
                "subject": "Order {}".format(self._id),
                "html": message})

    @classmethod
    def get_orders(cls, query=None):
        query = query or {}
        return [cls(**order) for order in Database.find(OrderConstants.COLLECTION, query)]
