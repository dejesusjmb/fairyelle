from flask import Blueprint, request, session, url_for, render_template, redirect

from src.models.admin.admin import Admin
import src.models.admin.errors as AdminErrors

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
                return redirect(url_for('orders.order_summary'))
        except AdminErrors.AdminError as e:
            return e.message

    return render_template('admin/login.html')  # Send the admin an error if their login was invalid


@admin_blueprint.route('/logout')
def logout_admin():
    session['email'] = None
    return redirect(url_for('home'))


