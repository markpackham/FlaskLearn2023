from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


# make sure to turn "Debug mode" ON so code changes are updated
# rather than constantly restarting the server
# set FLASK_DEBUG=1
# has to run via
# flask --app .\market.py run
# or short way if you just want to type 'flask run'
# set FLASK_APP=market.py


# @app.route('/about/<username>')
# def about_page(username):
#     return f"<h1>This is the about page of {username}</h1>"

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')



@app.route('/market')
def market_page():
    items = [
        {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
        {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
        {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
    ]
    return render_template('market.html', items=items)


@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')