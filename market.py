from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template('home.html')


# make sure to turn "Debug mode" ON so code changes are updated
# rather than constantly restarting the server
# set FLASK_DEBUG=1
# has to run via
# flask --app .\market.py run

# @app.route('/about/<username>')
# def about_page(username):
#     return f"<h1>This is the about page of {username}</h1>"
