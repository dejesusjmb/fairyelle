from flask import Blueprint, render_template

order_blueprint = Blueprint('orders',  __name__)


@order_blueprint.route('/checkout')
def checkout():
    return render_template('checkout.html')
