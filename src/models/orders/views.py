from collections import defaultdict
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request, session
import src.models.admin.decorators as admin_decorators
from src.models.customers.customer import Customer
from src.models.items.item import Item
from src.models.orders.order import Order

order_blueprint = Blueprint('orders',  __name__)


def initialize_cart():
    session['cart'] = defaultdict(int)
    session['number_of_items_in_cart'] = 0


@order_blueprint.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_id = request.form['item_id']
    quantity = int(request.form['quantity'])

    if 'cart' not in session:
        initialize_cart()

    if item_id in session['cart']:
        session['cart'][item_id] += quantity
    else:
        session['cart'][item_id] = quantity
    session['number_of_items_in_cart'] += quantity

    return redirect(request.referrer)


@order_blueprint.route('/edit_cart', methods=['GET', 'POST'])
def edit_cart():
    item_id = request.args['item_id']
    action = request.args['action']

    if action == 'add':
        session['cart'][item_id] += 1
        session['number_of_items_in_cart'] += 1
    else:
        if session['cart'][item_id] <= 1:
            del session['cart'][item_id]
        else:
            session['cart'][item_id] -= 1
        session['number_of_items_in_cart'] -= 1

    return redirect(request.referrer)


@order_blueprint.route('/cart')
def cart():
    items = []
    total = 0

    for item_id, quantity in session['cart'].items():
        item = Item.find_by_id(item_id)
        item_details = item.json()
        item_details['subtotal'] = quantity * item.price
        items.append(item_details)
        total += item_details['subtotal']

    return render_template('cart.html', items=items, total=total)


@order_blueprint.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        items = session['cart']
        name = request.form['name']
        contact_number = request.form['contactNumber']
        address = request.form['address']
        landmarks = request.form['landmarks']
        notes = request.form['notes']
        total_price = request.form['total']
        delivery = request.form['delivery']

        customer = Customer(name, contact_number, address, landmarks)
        customer.save_to_mongo()

        order = Order(customer._id, items, total_price, delivery, notes)
        order.save_to_mongo()
        order.send_notification()

        initialize_cart()

        return redirect(url_for('.acknowledge_order', order_id=order._id))

    items = []
    total = 0

    for item_id, quantity in session['cart'].items():
        item = Item.find_by_id(item_id)
        item_details = item.json()
        item_details['subtotal'] = quantity * item.price
        items.append(item_details)
        total += item_details['subtotal']

    return render_template('checkout.html', items=items, total=total)


@order_blueprint.route('/acknowledge')
def acknowledge_order():
    order = Order.find_by_id(request.args['order_id'])
    return render_template('acknowledge.html', order=order.summary)


@order_blueprint.route('/summary')
@admin_decorators.requires_admin_permissions
def order_summary():
    status = request.args['status']
    orders = Order.get_orders(status=status)
    orders = [order.summary for order in orders]
    return render_template('admin/summary.html', orders=orders)


@order_blueprint.route('/edit_status')
@admin_decorators.requires_admin_permissions
def edit_order_status():
    status = request.args['status']
    order_id = request.args['order_id']

    order = Order.find_by_id(order_id=order_id)
    order.status = status
    order.save_to_mongo()

    return redirect(request.referrer)
