from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.event import listen
from app import db, bcrypt
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement="auto")
    username = Column(String(32), unique=True, nullable=False)
    password = Column(String(64), nullable=False)
    admin = Column(Boolean, default=False)
    date_created = Column(DateTime(), server_default=func.now())
    
    def __repr__(self): return f"User('{self.username}', '{self.password}')"

def createDefaultUsers(target, connection, **kw):
    default_user_details = [{
        'username': 'admin',
        'password': 'Password123',
        'admin': True
    }, {
        'username': 'DSmart',
        'password': 'DSmart1',
        'admin': True
    }, {
        'username': 'JWilliams',
        'password': 'JWilliams1',
        'admin': True
    }, {
        'username': 'TLovell',
        'password': 'TLovell1',
        'admin': True
    }, {
        'username': 'CSamm',
        'password': 'CSamm1',
        'admin': True
    }]
    try:
        for user_details in default_user_details:
            hashed_password = sha256(user_details['password'].encode('utf-8')).hexdigest()
            user = User(user_details['username'], hashed_password, user_details['admin'])
            db.session.add(user)
        db.session.commit()
        print("Successfully created {0} users".format(len(default_user_details)))
    except Exception as e:
        print(e)
        db.session.rollback()

def createNewUser(username, password):
	try:
		hashed_password = sha256(password.encode('utf-8')).hexdigest()
		user = User(username, hashed_password, False)
		db.session.add(user)
		db.session.commit()
		print("Successfully created user %s", username)
	except Exception as e:
		print(e)
		db.session.rollback()

#listen(User.__table__, 'after_create', createDefaultUsers)