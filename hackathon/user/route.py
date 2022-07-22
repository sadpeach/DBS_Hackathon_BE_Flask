from flask import Flask, request, jsonify, Blueprint, make_response
import jwt
import json
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from functools import wraps
from hackathon.user.processor import UserProcessor
from hackathon import dbhelper
from hackathon.dbhelper import engine
from sqlalchemy.orm import sessionmaker
from hackathon import ormclasses

from flask_jwt_extended import create_access_token, unset_jwt_cookies, jwt_required, JWTManager, get_jwt_identity

user_blueprint = Blueprint("user_blueprint",__name__)
db = SQLAlchemy()

@user_blueprint.route('/login', methods=['POST'])
def login():
    userid = request.json.get("user", None)
    password = request.json.get("password", None)
    # check if user exists
    user_exists = ormclasses.User.query.filter_by(username = userid).first()
    if user_exists and password =="password":
        access_token = create_access_token(identity=user_exists.User_ID)
        response = {"access_token": access_token}
        return response, 200
    return {"msg": "Wrong credentials"}, 401

@user_blueprint.route('/logout',methods=['POST'])
def logout():
    response = jsonify({"msg": "User logged out"})
    return response

    
@user_blueprint.route('/getCurrency', methods=["GET"])
def getCurrency():
    # if request.method =="GET":
    # else
    return {"msg": "Currency"}

@user_blueprint.route('/getExchangeRate', methods=["GET"])
def getExchangeRate():
    exchangeRate = []
    content = {}
    try:
        data = data = db.engine.execute(text('SELECT * FROM multicurrency'))
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

@user_blueprint.route('/createNewTransaction', methods=['POST'])
def create_new_transaction():
    content : dict = request.get_json()   # type: ignore

    for k in [\
        'wallet_id', 'debit_id', 'debit_currency', 'debit_amount', 'credit_id', 'credit_currency', 'credit_amount',
        'description']:
        if k not in content:
            return jsonify({
                'err' : f'JSON key {k} not found'
            }), 400
    
    ''' created_by, updated_by'''

    Session = sessionmaker(bind=engine)
    session = Session()

    # validate that wallet exists
    wallet_id = content['wallet_id']
    wallet = session.query(ormclasses.Wallet)\
        .filter_by(id = content['wallet_id'])\
        .first()

    if wallet is None:
        return jsonify({'err' : f'Wallet {wallet_id} is not found'}), 400

    # ensure both currencies EXIST before proceeding

    credit_curr = session.query(ormclasses.Currency)\
        .filter_by(id = content['credit_id'])\
        .first()

    if credit_curr is None:
            return jsonify({'err' : f'Currency {credit_curr.id} is not found'}), 400

    debit_curr = session.query(ormclasses.Currency)\
        .filter_by(id = content['credit_id'])\
        .first()

    if debit_curr is None:
            return jsonify({'err' : f'Currency {debit_curr.id} is not found'}), 400
    
    session.query(ormclasses.Currency)\
        .filter_by(id = credit_curr.id)\
        .update({ormclasses.Currency.amount : ormclasses.Currency.amount - content['credit_amount']})

    session.query(ormclasses.Currency)\
        .filter_by(id = debit_curr.id)\
        .update({ormclasses.Currency.amount : ormclasses.Currency.amount + content['debit_amount']})  

    transaction : ormclasses.Transaction = ormclasses.Transaction(
        wallet_id= wallet_id,
        debit_id= content['debit_id'],
        debit_currency=content['debit_currency'],
        debit_amount=content['debit_amount'],
        credit_id= content['credit_id'],
        credit_currency=content['credit_currency'],
        credit_amount=content['credit_amount'],
        description=content['description'],
        created_by = wallet.user_id,
        updated_by= wallet.user_id
    )

    session.add(transaction)
    session.commit()
    
    return jsonify({'err' : 'success'}), 200


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

