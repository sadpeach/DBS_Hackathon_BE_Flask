from flask import Flask, request, jsonify, Blueprint, make_response
import jwt
import json
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from functools import wraps
from hackathon.user.processor import UserProcessor
from hackathon import dbhelper
from hackathon import ormclasses

from flask_jwt_extended import create_access_token, unset_jwt_cookies, jwt_required, JWTManager, get_jwt_identity
from hackathon import db

user_blueprint = Blueprint("user_blueprint",__name__)
#db = SQLAlchemy(user_blueprint)

@user_blueprint.route('/login', methods=['POST'])
def login():
    userid = request.json.get("user", None)
    password = request.json.get("password", None)

    Session = sessionmaker(bind = dbhelper.engine)
    session = Session()

    user = session.query(ormclasses.User).filter_by(username = userid).filter_by(password = password).first()

    # check if user exists
    # user_exists = ormclasses.User.query.filter_by(username = userid).first()
    if user is not None:
        #access_token = create_access_token(identity=user.id)
        access_token = 'testaccesstoken'
        response = {"access_token": access_token, "user_id":user.id}
        return response, 200
    return {"msg": "Wrong credentials"}, 404

@user_blueprint.route('/logout',methods=['POST'])
def logout():
    response = jsonify({"msg": "User logged out"})
    return response, 200

    
@user_blueprint.route('/getCurrency', methods=["GET"])
def getCurrency():
    currency = []
    content = {}
    try:
        
        Session = sessionmaker(bind = dbhelper.engine)
        session = Session()

        data = session.query(ormclasses.Currency).all()

        if data is None or len(data) == 0:
            message = jsonify(message='No data Found')
            return make_response(message,404)

        for result in data:
            content = {'wallet_id': result.wallet_id, 'currency': result.currency,'amount':result.amount}
            currency.append(content)
            content = {}
        return make_response(jsonify(currency), 200)

    except (RuntimeError, TypeError, NameError) as e:
        print(e)
        message = jsonify(message='Server Error')
        return make_response(message, 500)

@user_blueprint.route('/getExchangeRate', methods=["GET"])
def getExchangeRate():
    exchangeRate = []
    content = {}

    Session = sessionmaker(bind = dbhelper.engine)
    session = Session()

    data = session.query(ormclasses.ExchangeRate).all()

    if data is None or len(data) == 0:
        message = jsonify(message='No data Found')
        return make_response(message,404)

    for result in data:
        content = {'base_currency': result.base_currency, 'exchange_currency': result.exchange_currency,'rate':result.rate}
        exchangeRate.append(content)
        content = {}        

    return make_response(jsonify(exchangeRate),200)

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

