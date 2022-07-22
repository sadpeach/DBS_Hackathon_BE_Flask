import hackathon.ormclasses as orc
from hackathon.ormclasses import User
import hackathon.dbhelper as dbh
from hackathon.dbcreds import ENGINE_STR

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=dbh.engine)
session = Session()

user : User|None = session.query(User)\
        .filter_by(username = 'user101')\
        .first()

print(ENGINE_STR)