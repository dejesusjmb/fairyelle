# from flask import Blueprint, render_template, request, redirect, url_for
# import src.models.admin.decorators as admin_decorators
# from src.models.customers.customer import Customer
# from src.common.database import Database
# import src.models.customers.constants as CustomerConstants
#
# customer_blueprint = Blueprint('customers',  __name__)
#
#
# @customer_blueprint.route('/')
# @admin_decorators.requires_admin_permissions
# def customers():
#     items = [Customer(**customer) for customer in Database.find(CustomerConstants.COLLECTION, {})]
#     return render_template('admin/customers.html', items=items)
