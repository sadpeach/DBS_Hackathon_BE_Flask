from bson import ObjectId
from hackathon import db
collection = db["user"]

class UserProcessor:

    def getUserByUserId(id):
        user = collection.find_one({"_id":ObjectId(id)})
        return user
    
    def getUserByUserNameAndPassword(email,password):
        user = collection.find_one({"email":email, 'password':password})
        return user
    

