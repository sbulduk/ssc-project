from base.app_config import AppConfig
from dataclasses import dataclass

app=AppConfig.InitApp()
db=AppConfig.InitDB()

@dataclass
class Role(db.Model):
	__tablename__="roles"

	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(16),nullable=False)
	explanation=db.Column(db.String(512),nullable=False)
	isactive=db.Column(db.Boolean,nullable=False)

	def __init__(self,name,explanation,isactive):
		self.name=name
		self.explanation=explanation
		self.isactive=isactive