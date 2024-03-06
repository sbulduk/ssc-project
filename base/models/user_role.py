from flask_sqlalchemy import Table,ForeignKey,Column,Integer,String,Boolean

userRole=Table("usersroles",
			   Column("user_id",Integer,ForeignKey("users.id")),
			   Column("role_id",Integer,ForeignKey("roles.id"))
			   )