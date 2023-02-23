from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"

# make sure to turn "Debug mode" ON so code changes are updated
# rather than constantly restarting the server
# set FLASK_DEBUG=1
# has to run via
# flask --app .\market.py run
