from bson import ObjectId
from flask import Flask, request, jsonify, Blueprint
from hackathon import db
import jwt
import json
import pymongo
import os
from datetime import datetime, timedelta
from functools import wraps
from processor import UserProcessor

user_blueprint = Blueprint("user_blueprint",__name__)

collection = db["user"]

@user_blueprint.route('/api/v1/login',methods=['POST'])
def login():

    data = request.get_json()
    email = data['email']
    password = data['password']
    token = None

    user =  UserProcessor.getUserByUserNameAndPassword(email,password)

    if user is None:
        return jsonify({
            "status" : "error",
            "message" : "user does not exist"
        }), 401
    
    else:

        #generate jwt token
        token = jwt.encode({
            '_id' : user['_id'],
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, os.environ.get("SECRET_KEY"))

        user['token'] = token.decode('UTF-8')

        return jsonify({
            "status" : "success",
            "data" : json.loads(json.dumps(user,default=str))
        }), 200

@user_blueprint.route('/api/v1/register',methods=['POST'])
def register():

    data = request.get_json()
    user = User(data['email'],data['password'],data['name']).asdict()
    account = collection.insert_one(user)
    user = collection.find_one({"_id":account.inserted_id}) 

    return jsonify({
            "status" : "success",
            "message" : "user successfully created",
            "data" : json.loads(json.dumps(user,default=str))
        }), 200


# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, os.environ.get("SECRET_KEY"))
            current_user = collection.find_one({"_id":ObjectId(data["_id"])})

        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated

