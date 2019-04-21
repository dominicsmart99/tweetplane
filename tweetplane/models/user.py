from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.event import listen
from tweetplane import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement="auto")
    username = Column(String(32), unique=True, nullable=False)
    password = Column(String(64), nullable=False)
    admin = Column(Boolean, default=False)
    date_created = Column(DateTime(), server_default=func.now())
    
    def __repr__(self): return f"User('{self.username}', '{self.admin}')"

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
            hashed_password = bcrypt.generate_password_hash(user_details['password']).decode('utf-8')
            user = User(username=user_details['username'], password=hashed_password, admin=user_details['admin'])
            db.session.add(user)
        db.session.commit()
        print("Successfully created {0} users".format(len(default_user_details)))
    except Exception as e:
        print(e)
        db.session.rollback()


listen(User.__table__, 'after_create', createDefaultUsers)