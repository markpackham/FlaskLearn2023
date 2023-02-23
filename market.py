from flask import Flask, render_template
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
    return render_template('market.html', item_name='Phone')

