import hackathon.ormclasses as orc
from hackathon.ormclasses import User
import hackathon.dbhelper as dbh

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=dbh.engine)
session = Session()

user : User|None = session.query(User)\
        .filter_by(username = 'user101')\
        .first()

print(f'{user.username}, {user.password}')