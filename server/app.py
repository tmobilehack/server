import os
import json

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

# delete this
from random import random

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from resources.calc import Calc, Test

api = Api(app)

api.add_resource(Test, '/')
api.add_resource(Calc, '/api')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
