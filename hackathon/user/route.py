from flask import Flask, request, jsonify, Blueprint,make_response
from hackathon import db
import jwt
import json
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from functools import wraps
from hackathon.user.processor import UserProcessor

from flask_jwt_extended import create_access_token, unset_jwt_cookies, jwt_required, JWTManager, get_jwt_identity

user_blueprint = Blueprint("user_blueprint",__name__)


@user_blueprint.route('/login', methods=['POST'])
def login():
    userid = request.json.get("user", None)
    password = request.json.get("password", None)
    # check if user exists
    user_exists = models.User.query.filter_by(Email=userid).first()
    if user_exists and password=="default": 
        #access_token = create_access_token(identity=userid)  
        access_token = create_access_token(identity=user_exists.User_ID)
        response = {"access_token":access_token}
        return response, 200
    return {"msg": "Wrong credentials"}, 401

@user_blueprint.route('/api/v1/login',methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user =  UserProcessor.getUserByUserNameAndPassword(email,password)

    return jsonify({
            "status" : "SUCCESS",
            "data": json.loads(json.dumps(user,default=str))
        }), 200
    
@user_blueprint.route('/getCurrency', methods=["GET"])
def getCurrency():
    data = []

@user_blueprint.route('/getExchangeRate', methods=["GET"])
def getExchangeRate():
    exchangeRate = []
    content = {}
    
    try:
        data = data = db.engine.execute(text('SELECT * FROM multicurrency'));
        if(data != ""):
            for result in data:
                content = {'base_currency': result['base_currency'], 'exchange_currency': result['exchange_currency'],'rate':result['rate']}
                exchangeRate.append(content)
                content = {}
            return make_response(jsonify(exchangeRate),200)
        else:
            message = jsonify(message='No data Found')
            return make_response(message,404)

    except (RuntimeError, TypeError, NameError):
        message = jsonify(message='Server Error')
        return make_response(message, 500)

# @user_blueprint.route('/api/v1/login',methods=['POST'])
# def login():

#     data = request.get_json()
#     email = data['email']
#     password = data['password']
#     token = None

#     user =  UserProcessor.getUserByUserNameAndPassword(email,password)

#     if user is None:
#         return jsonify({
#             "status" : "error",
#             "message" : "user does not exist"
#         }), 401
    
#     else:

#         #generate jwt token
#         token = jwt.encode({
#             '_id' : user['_id'],
#             'exp' : datetime.utcnow() + timedelta(minutes = 30)
#         }, os.environ.get("SECRET_KEY"))

#         user['token'] = token.decode('UTF-8')

#         return jsonify({
#             "status" : "success",
#             "data" : json.loads(json.dumps(user,default=str))
#         }), 200

# @user_blueprint.route('/api/v1/register',methods=['POST'])
# def register():

#     data = request.get_json()
#     user = User(data['email'],data['password'],data['name']).asdict()
#     account = collection.insert_one(user)
#     user = collection.find_one({"_id":account.inserted_id}) 

#     return jsonify({
#             "status" : "success",
#             "message" : "user successfully created",
#             "data" : json.loads(json.dumps(user,default=str))
#         }), 200


# # decorator for verifying the JWT
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         # jwt is passed in the request header
#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']
#         # return 401 if token is not passed
#         if not token:
#             return jsonify({'message' : 'Token is missing !!'}), 401
  
#         try:
#             # decoding the payload to fetch the stored details
#             data = jwt.decode(token, os.environ.get("SECRET_KEY"))
#             current_user = collection.find_one({"_id":ObjectId(data["_id"])})

#         except:
#             return jsonify({
#                 'message' : 'Token is invalid !!'
#             }), 401
#         # returns the current logged in users contex to the routes
#         return  f(current_user, *args, **kwargs)
  
#     return decorated

