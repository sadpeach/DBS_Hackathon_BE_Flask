from flask import Flask, Blueprint
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv

import os
import logging
import pymongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId


load_dotenv(find_dotenv())
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

'''
print("DB_URL:",os.environ.get("DB_URL"))
mongo = pymongo.MongoClient(os.environ.get("DB_URL"))
db = pymongo.database.Database(mongo,"dbs_hackathon")
'''

from hackathon.user.route import user_blueprint

app.register_blueprint(user_blueprint, url_prefix='/user')
