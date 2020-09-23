from flask import Blueprint, render_template

item_blueprint = Blueprint('items',  __name__)


@item_blueprint.route('/<string:item_id>')
def display_item(item_id):
    return render_template('product.html')
