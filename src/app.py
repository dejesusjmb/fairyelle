from flask import Flask, render_template
from src.common.database import Database
from src.models.orders.views import order_blueprint
from src.models.items.views import item_blueprint

app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = '123'


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    return render_template('home.html')


app.register_blueprint(order_blueprint, url_prefix='/orders')
app.register_blueprint(item_blueprint, url_prefix='/items')
