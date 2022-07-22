import hackathon.ormclasses as orc
from hackathon.ormclasses import User
import hackathon.dbhelper as dbh

from sqlalchemy.orm import sessionmaker

class UserProcessor:

    def getUserByUserId(userid):
        Session = sessionmaker(bind=dbh.engine)
        session = Session()

        user : User|None = session.query(User)\
            .filter_by(id = userid)\
            .first()

        return user
    
    def getUserByUserNameAndPassword(username,password):

        Session = sessionmaker(bind=dbh.engine)
        session = Session()

        user : User|None = session.query(User)\
            .filter_by(username = username)\
            .filter_by(password = password)\
            .first()
        return user
    

