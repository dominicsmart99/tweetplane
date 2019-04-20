from sqlalchemy import Column, String, Integer, Boolean

class User(db.Model):
	__tablename__ - 'users'
	username = Column(String(32), primary_key=True)
	password = Column(String(50), nullable=False)
	admin = Column(Boolean, default=False)

	def __init__(self, username, password, admin=False):
		self.username = username
		self.password = password
		self.admin = admin