from flask import Flask, render_template, session
from src.common.database import Database

app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = '123'


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    # del session['cart']
    # del session['number_of_items_in_cart']
    return render_template('home.html')


from src.models.orders.views import order_blueprint
from src.models.items.views import item_blueprint
from src.models.admin.views import admin_blueprint

app.register_blueprint(order_blueprint, url_prefix='/orders')
app.register_blueprint(item_blueprint, url_prefix='/items')
app.register_blueprint(admin_blueprint, url_prefix='/admin')
