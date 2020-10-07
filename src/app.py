from flask import Flask, render_template, session, request
from src.common.database import Database

app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = '123'


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/error')
def error():
    error_code = int(request.args['error_code'])
    error_message_map = {
        1: 'Invalid login credentials',
        2: 'You should be at least 21 years old to order'
    }
    return render_template('error.html', error_message=error_message_map[error_code])


from src.models.orders.views import order_blueprint
from src.models.items.views import item_blueprint
from src.models.admin.views import admin_blueprint

app.register_blueprint(order_blueprint, url_prefix='/orders')
app.register_blueprint(item_blueprint, url_prefix='/items')
app.register_blueprint(admin_blueprint, url_prefix='/admin')
