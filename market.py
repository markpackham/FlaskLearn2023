from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
# add extra config to "app" with key and value
# the value is a URI (link to a file, rather than a Url which links to a site)
# database used is store in /instance/market.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db = SQLAlchemy(app)

# make sure to turn "Debug mode" ON so code changes are updated
# rather than constantly restarting the server
# set FLASK_DEBUG=1
# has to run via
# flask --app .\market.py run
# or short way if you just want to type 'flask run'
# set FLASK_APP=market.py


