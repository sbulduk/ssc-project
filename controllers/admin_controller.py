from flask import Blueprint,request,jsonify
from base.models.user import User

apiAdmin=Blueprint("apiAdmin",__name__,url_prefix="/api/admin")

@apiAdmin.route("/")
def Index():
	return jsonify({"success":True,"data":f"Welcome to the admin page."})


@apiAdmin.route("/adduser",methods=["GET"])
def AddUser():
	try:
		username=request.form.get("username")
		email=request.form.get("email")
		password=request.form.get("password")
		isactive=request.form.get("isactive")
		isactive=bool(isactive.lower()=="true")
		
		User.add(username,email,password,isactive)
		return jsonify({"success":True,"message":"User added successfully."})
	except Exception as e:
		print(e)
		return jsonify({"success":False,"message":"An error occured during the process!"})