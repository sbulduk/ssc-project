from flask import Blueprint,jsonify
from services.virtualization.vm import VM

apiServer=Blueprint("apiServer",__name__,url_prefix="/api/servers")

@apiServer.route("/",methods=["GET"])
def Index():
	virtualMachineManager=VM()
	serviceInstance=virtualMachineManager.Connect()
	serverList=virtualMachineManager.GetVirtualMachineList(serviceInstance)
	return jsonify({"success":True,"body":serverList})

@apiServer.route("/<int:id>",methods=["GET"])
def GetServerById(id):
	return jsonify({"success":True,"message":f"Selected Server is: {id}."})

# @apiServer.route("/<int:id>/<str:opr>",methods=["POST"])
# def PowerOnServer(id,opr):
# 	selectedVirtualMachine=virtualMachineManager.GetVirtualMachineById(id)
# 	selectedVirtualMachine.PowerOn()