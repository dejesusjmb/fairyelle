from datetime import datetime, timedelta

from flask import Blueprint, request, session, url_for, render_template, redirect

from src.common.database import Database
from src.models.admin.admin import Admin
from src.models.customers.customer import Customer
import src.models.admin.errors as AdminErrors
import src.models.admin.decorators as admin_decorators
import src.models.customers.constants as CustomerConstants

admin_blueprint = Blueprint('admin', __name__)
# There is only one admin for now and that is the admin.


@admin_blueprint.route('/', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if Admin.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for('orders.order_summary', status='open'))
        except AdminErrors.AdminError as e:
            return redirect(url_for('error', error_code=1))

    return render_template('admin/login.html')  # Send the admin an error if their login was invalid


@admin_blueprint.route('/logout')
def logout_admin():
    session['email'] = None
    return redirect(url_for('home'))


@admin_blueprint.route('/customers')
@admin_decorators.requires_admin_permissions
def customers():
    ordered_at = request.args.get('ordered_at')

    query = {}
    if ordered_at:
        ordered_at = datetime.strptime(ordered_at, '%b-%d-%Y')
        next_day = (ordered_at + timedelta(days=1)).date()
        next_day = datetime(next_day.year, next_day.month, next_day.day)
        query['ordered_at'] = {'$gte': ordered_at, '$lt': next_day}

    customers = Customer.get_customers(query=query)
    query['ordered_at'] = request.args.get('ordered_at')
    return render_template('admin/customers.html', customers=customers, query=query)
