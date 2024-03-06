# from services.ad.ad_credentials import ADCredentials
# from pyad import *
# from flask import jsonify
# import subprocess

# class AD(object):
# 	def __init__(self):
# 		self.host,self.user,self.password=ADCredentials.GetCredentials()

# 	def Connect(self):
# 		try:
# 			self.dc=pyad.ADDomainConnection(self.host,self.user,self.password,use_ssl=True)
# 			print(f"Connection established successfully.")
# 			return self.dc
# 		except Exception as e:
# 			print(f"Error occured while connecting to AD domain: {e}")

# 	def GetAllGroups(self):
# 		try:
# 			groupList=self.dc.get_all_groups()
# 			groupNames=[group.name for group in groupList]
# 			if groupNames.count==0:
# 				return jsonify({"success":True,"data":f"No groups found."})
# 			return jsonify({"success":True,"data":groupNames})
# 		except Exception as e:
# 			return jsonify({"success":False,"data":f"Failed to list groups: {e}"}),500

# 	def AddNewGroup(self,groupName,groupDescription=None):
# 		command=f"dsadd group -cn \"{groupName}\""
# 		if groupDescription:
# 			command+=f" -desc \"{groupDescription}\""
# 		try:
# 			return jsonify({"success":True,"data":f"Command: {command}"})
# 			# subprocess.run(command,shell=True,check=True)
# 		except Exception as e:
# 			return jsonify({"success":False,"data":f"Error while adding the group [{groupName}]: {e}"})
		
# 	def UpdateGroup(self,groupName,newName,newDescription):
# 		commandList=[]
# 		if newName:
# 			commandList.append(f"dsmod group -cn \"{groupName}\" -rename \"{newName}\"")
# 		if newDescription:
# 			commandList.append(f"dsmod group -cn \"{groupName}\" -desc \"{newDescription}\"")
# 		for command in commandList:
# 			try:
# 				return jsonify({"success":True,"data":f"Command: {command}"})
# 				# subprocess.run(command,shell=True,check=True)
# 			except Exception as e:
# 				return jsonify({"success":False,"data":f"Error while processing command [{command}]\nError details: {e}"})

# 	def DeleteGroup(self,groupName):
# 		command=f"dsrm group \"{groupName}\" -force"
# 		try:
# 			return jsonify({"success":True,"data":f"Command: {command}"})
# 			# subprocess.run(command,shell=True,check=True)
# 		except Exception as e:
# 			return jsonify({"success":False,"data":f"Error while deleting group [{groupName}]\nError details: {e}"})
		
# 	def GetUsersByGroup(self,groupName):
# 		try:
# 			selectedGroup=self.dc.get_group_by_name(groupName)
# 			usersList=selectedGroup.members
# 			usersNames=[user.name for user in usersList]
# 			if usersNames.count==0:
# 				return jsonify({"success":True,"data":f"No users in the group [{groupName}]"})
# 			return jsonify({"success":True,"data":usersNames})
# 		except Exception as e:
# 			return jsonify({"success":False,"data":f"Failed to list users: {e}"}),500

# 	def AddNewUser(self,group,user):
# 		pass

# 	def UpdateUser(self,groupName,userName):
# 		pass