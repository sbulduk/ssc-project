from flask_sqlalchemy import SQLAlchemy
from flask import Flask,jsonify

class AppConfig(object):
	@staticmethod
	def InitDB():
		return SQLAlchemy()

	@staticmethod
	def InitApp():
		app=Flask(__name__)
		app.config["SQLALCHEMY_DATABASE_URI"]="mssql+pyodbc://sa:Sbulduk2023!@192.168.31.131:1433/ssc?driver=SQL+Server"
		return app

	@staticmethod
	def RegisterBlueprints(app):
		from controllers.ad_controller import apiAD
		from controllers.admin_controller import apiAdmin
		from controllers.server_controller import apiServer
		from controllers.user_controller import apiUser

		if "apiAD" not in app.blueprints:
			app.register_blueprint(apiAD)
		if "apiAdmin" not in app.blueprints:
			app.register_blueprint(apiAdmin)
		if "apiServer" not in app.blueprints:
			app.register_blueprint(apiServer)
		if "apiUser" not in app.blueprints:
			app.register_blueprint(apiUser)

	@staticmethod
	def CreateAll(app,db):
		try:
			with app.app_context():
				db.init_app(app)
				db.create_all()
		except Exception as e:
			with app.app_context():
				import traceback
				traceback.print_exc()
				message=jsonify({"success":False,"body":f"Program could not be run.\nError details: {e}"})
				print(str(message))

	@staticmethod
	def RunApp():
		app=AppConfig.InitApp()
		db=AppConfig.InitDB()
		AppConfig.RegisterBlueprints(app)
		AppConfig.CreateAll(app,db)
		return app