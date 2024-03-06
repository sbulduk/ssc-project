from flask import Blueprint,request,jsonify
from services.ad.ad import AD

apiAD=Blueprint("apiAD",__name__,url_prefix="/api/ad")
activeDirectoryService=AD()

@apiAD.route("/",methods=["GET"])
def Index():
	try:
		return jsonify({"success":True,"message":"Welcome to Active Directory Service"})
	except Exception as e:
		print(e)
		return jsonify({"success":False,"message":"An error occured during the process!"})
	
@apiAD.route("/groups",methods=["GET"])
def Groups():
	return activeDirectoryService.GetAllGroups()

@apiAD.route("/groups/<string:groupName>")
def Users(groupName):
	return activeDirectoryService.GetUsersByGroup(groupName)