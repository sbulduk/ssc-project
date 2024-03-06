from base.app_config import AppConfig
from dataclasses import dataclass

app=AppConfig.InitApp()
db=AppConfig.InitDB()

@dataclass
class User(db.Model):
	__tablename__="users"
	
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(32),nullable=False)
	email=db.Column(db.String(64),unique=True,nullable=False)
	password=db.Column(db.String(256),nullable=False)
	role=db.Column(db.Integer,nullable=False)
	isactive=db.Column(db.Boolean,nullable=False)

	def __init__(self,username,email,password,isactive):
		self.username=username
		self.email=email
		self.password=password
		self.isactive=isactive