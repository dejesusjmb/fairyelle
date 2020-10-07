from flask import Blueprint, render_template, request, redirect, url_for
import src.models.admin.decorators as admin_decorators
from src.models.items.item import Item
from src.common.database import Database
import src.models.items.constants as ItemConstants

item_blueprint = Blueprint('items',  __name__)


@item_blueprint.route('/')
@admin_decorators.requires_admin_permissions
def items():
    items = [Item(**item) for item in Database.find(ItemConstants.COLLECTION, {})]
    return render_template('admin/items.html', items=items)


@item_blueprint.route('/new', methods=['GET', 'POST'])
@admin_decorators.requires_admin_permissions
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        image_url = request.form['image_url']
        category = request.form['category']
        subcategory = request.form['subcategory']

        item = Item(name, price, category, subcategory, description, image_url)
        item.save_to_mongo()

    return render_template('admin/new_item.html')


@item_blueprint.route('/edit/<string:item_id>', methods=['GET', 'POST'])
@admin_decorators.requires_admin_permissions
def edit_item(item_id):
    item = Item.find_by_id(item_id)
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        image_url = request.form['image_url']
        subcategory = request.form['subcategory']

        item.name = name
        item.price = price
        item.description = description
        item.image_url = image_url
        item.category = subcategory
        item.save_to_mongo()
        return redirect(url_for('.items'))

    return render_template('admin/edit_item.html', item=item)


@item_blueprint.route('/delete/<string:item_id>')
@admin_decorators.requires_admin_permissions
def delete_item(item_id):
    Item.find_by_id(item_id).delete()
    return redirect(url_for('.items'))


@item_blueprint.route('/category/<string:category>')
def display_items_by_category(category):
    items = Item.find_by_category(category)
    return render_template('product_list.html', category=category, items=items)


@item_blueprint.route('/subcategory/<string:subcategory>')
def display_items_by_subcategory(subcategory):
    items = Item.find_by_subcategory(subcategory)
    return render_template('product_list.html', category=subcategory, items=items)


@item_blueprint.route('/<string:item_id>')
def display_item(item_id):
    item = Item.find_by_id(item_id)
    return render_template('product.html', item=item)
