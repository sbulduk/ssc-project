from services.ad.ad_credentials import ADCredentials
import subprocess
from flask import jsonify

class AD(object):
	def __init__(self):
		self.server,self.user,self.password,self.searchBase=ADCredentials.GetCredentials()

	def RunCommand(self,command):
		try:
			fullCommand=(f"plink -ssh {self.user}@{self.server} -pw {self.password} {command}")
			result=subprocess.run(fullCommand,shell=True,capture_output=True,text=True,check=True)
			return result.stdout.strip().split("\n")
		except Exception as e:
			return jsonify({"success":False,"data":f"Error while running command: {e}"})

	def GetAllGroups(self):
		try:
			command=f"dsquery group -s {self.server} -u {self.user} -p {self.password}"
			return self.RunCommand(command)
		except Exception as e:
			return jsonify({"success":False,"data":f"Error while loading groups. Error details: {e}"})

	def AddNewGroup(self,groupName,groupDescription=None):
		try:
			command=f"dsadd group -s {self.server} -u {self.user} -p {self.password} -cn {groupName}"
			if groupDescription:
				command+=f" -desc \"{groupDescription}\""
			return self.RunCommand(command)
		except Exception as e:
			return jsonify({"success":False,"data":f"Error while adding new groups. Error details: {e}"})
		
	def UpdateGroup(self,groupName,groupNewName,newDescription):
		try:
			command=f"dsmod group -s {self.server} -u {self.user} -p {self.password} -dn {groupName}"
			if groupNewName:
				command+=f" -newname {groupNewName}"
			if newDescription:
				command+=f" -desc \"{newDescription}\""
			return self.RunCommand(command)
		except Exception as e:
			return jsonify({"success":False,"data":f"Error while updating group - [{groupName}] info. Error details: {e}"})

	# def RemoveGroup(self,groupName): # Also deletes the users, sharing the deleted group, from the server.
	# 	try:
	# 		usersinGroup=self.GetUsersByGroup(groupName)
	# 		for userName in usersinGroup:
	# 			self.RemoveUser(userName)
	# 		commanRemoveGroup=f"dsrm {groupName}"
	# 		resultRemoveGroup=self.RunCommand(commanRemoveGroup)
	# 		return resultRemoveGroup
	# 	except Exception as e:
	# 		return jsonify({"success":False,"data":f"Error during process. Error details: {e}"})
		
	def RemoveGroup(self,groupName):
		try:
			command=(
				f"dsrm group -s {self.server} -u {self.user} -p {self.password} "
				f"-dn {groupName}"
			)
			try:
				resultRemoveGroup=self.RunCommand(command)
				if resultRemoveGroup.get("success",False):
					return jsonify({"success":True,"data":f"Group [{groupName}] removed successfully."})
				else:
					return resultRemoveGroup
			except Exception as resultRemoveGroupError:
				return jsonify({"success":False,"data":f"Error while deleting the group [{groupName}]. Error details: {resultRemoveGroupError}"})
		except Exception as e:
			return jsonify({"success":False,"data":f"Error while deleting the group [{groupName}]. Error details: {e}"})

	def GetUsersByGroup(self,groupName):
		try:
			command=(
				f"dsget group -s {self.server} -u {self.user} -p {self.password} "
				f"-members -dn {groupName}"
			)
			return self.RunCommand(command)
		except Exception as e:
			return jsonify({"success":False,"data":f"Error while loading the users in the group - [{groupName}]. Error details: {e}"})
		
	def GetUserDetails(self,userName):
		command=f"dsquery user -samid {userName}"
		result=self.RunCommand(command)
		if result.get("success",False):
			userDetails=self.ParseUserDetails(result.get("data",""))
			return jsonify({"success":True,"data":userDetails})
		else:
			return result
		
	def ParseUserDetails(self,rawUserData):
		userDetails={}
		lines=rawUserData.split("\n")
		for line in lines:
			if line.strip():
				key,value=line.split(":",1)
				userDetails[key.strip()]=value.strip()
		return userDetails
	
	# def ParseUserDetails(self,rawUserData): #Alternative to the "ParseUserDetails" function.
	# 	userDetails={}
	# 	for line in rawUserData.splitlines():
	# 		if line.startswith("dn:"):
	# 			userDetails["dn"]=line.split(" ")[-1]
	# 		elif line.startswith("samaccountname:"):
	# 			userDetails["username"]=line.split(": ")[1]
	# 		elif line.startswith("givenname:"):
	# 			userDetails["first_name"]=line.split(": ")[1]
	# 		elif line.startswith("sn:"):
	# 			userDetails["last_name"]=line.split(": ")[1]
	# 		elif line.startswith("userprincipalname:"):
	# 			userDetails["email"]=line.split(": ")[1]
	# 		elif line.startswith("memberof:"):
	# 			if "groups" not in userDetails:
	# 				userDetails["groups"]=[]
	# 			userDetails["groups"].append(line.split("CN=")[1].split(",")[0])
	# 	return userDetails

	# def AddUsertoGroup(self,groupName,userName,password): # Alternative to both "AddUser" and "SetUsertoGroups" functions.
	# 	try:
	# 		commandAddUser=(
	# 			f"dsadd user -s {self.server} -u {self.user} -p {self.password} "
	# 			f"-samid {userName} -upn {userName}@domain.com -fn {userName} -pwd {password}"
	# 		)
	# 		try:
	# 			resultAddUser=self.RunCommand(commandAddUser)
	# 			if resultAddUser.get("success",False):
	# 				commandAddUsertoGroup=(
	# 					f"dsmod group -s {self.server} -u {self.user} -p {self.password} "
	# 					f"-dn {groupName} -addmbr {userName}"
	# 				)
	# 				try:
	# 					resultAddUsertoGroup=self.RunCommand(commandAddUsertoGroup)
	# 					if not resultAddUsertoGroup.get("success",False):
	# 						self.RemoveUser(userName)
	# 						return resultAddUsertoGroup
	# 				except Exception as addUsertoGroupError:
	# 					return jsonify({"success":False,"data":f"Error while adding new user [{userName}] to selected group [{groupName}]. Error details: {addUsertoGroupError}"})
	# 			return resultAddUser
	# 		except Exception as addUserError:
	# 			return jsonify({"success":False,"data":f"Error while adding new user. Error details: {addUserError}"})
	# 	except Exception as e:
	# 		return jsonify({"success":False,"data":f"Error while loading the users in the group {groupName}. Error details: {e}"})

	def AddUser(self,userName,password,email=None,isActive=True):
		try:
			command=(
				f"dsadd user -s {self.server} -u {self.user} -p {self.password} "
				f"-samid {userName} -upn {userName}@domain.com -fn {userName} -pwd {password}"
			)
			if email:
				command+=f" -email {email}"
			if not isActive:
				command+=f" -disabled"
			try:
				result=self.RunCommand(command)
				return result
			except Exception as resultAddUserError:
				return jsonify({"success":False,"data":f"Error while adding new user [{userName}]. Error details: {resultAddUserError}"})
		except Exception as e:
			return jsonify({"success":False,"data":f"Error while adding new user [{userName}]. Error details: {e}"})
		
	def SetUsertoGroup(self,userName,groups=None):
		try:
			if not groups:
				return jsonify({"success":False,"data":f"No groups provided to set the user [{userName}]."})
			for group in groups:
				command=(
					f"dsmod group -s {self.server} -u {self.user} -p {self.password} "
					f"-dn {group} -addmbr {userName}"
				)
				try:
					resultSetUsertoGroup=self.RunCommand(command)
					if not resultSetUsertoGroup.get("success",False):
						return resultSetUsertoGroup
				except Exception as resultSetUsertoGroupError:
					return jsonify({"success":False,"data":f"Error while setting user [{userName}] to group [{group}]. Error details: {resultSetUsertoGroupError}"})
			return jsonify({"success":True,"data":f"User [{userName}] set to groups: {', '.join(groups)} successfully."})
		except Exception as e:
			return jsonify({"success":False,"data":f"Error while setting user [{userName}] to group [groupName]. Error details: {e}"})

	def UpdateUser(self,userName,newUserName=None,newPassword=None,newGroup=None):
		command=f"net user {userName}"
		if newUserName:
			command+=f" /username:{newUserName}"
		if newPassword:
			command+=f" {newPassword}"
		if newGroup:
			pass
		try:
			result=self.RunCommand(command)
			if result.get("success",False):
				return jsonify({"success":True,"data":f"User updated successfully."})
			else:
				return jsonify({"success":False,"data":f"Failed to update user [{userName}]."})
		except Exception as e:
			return jsonify({"success":False,"data":f"An error occured during update. Error details: {e}"})

	def RemoveUser(self,userName):
		command=(
			f"dsrm -noprompt -s {self.server} -u {self.user} -p {self.password} "
			f"-c -subtree -dn CN={userName},CN=Users,{self.searchBase}"
		)
	
	# TODO: Will be checked!!!
	def RemoveUserFromGroup(self,groupName,userName):
		command=f"dsmod group -s {self.server} -u {self.user} -p {self.password} -dn {groupName} -rmmbr {userName}"
		return self.RunCommand(command)
	
	def AddPermission(self,name,resource,permission):
		command=f"icacls {resource} /grant {name}:{permission}"
		return self.RunCommand(command)

	def RemovePermission(self,name,resource,permission):
		command=f"icacls {resource} /remove {name}:{permission}"
		return self.RunCommand(command)