"""
Initialize the flask
and run the app
Initialize sql alchemy

"""

from flask import Flask
from flask_mongoalchemy import MongoAlchemy
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo


app = Flask(__name__)
Bootstrap(app)
app.config.from_pyfile('config.py')

# create the db
db = MongoAlchemy(app)
mongodb = PyMongo(app)



from views import *
if __name__ == '__main__':
    app.run()
