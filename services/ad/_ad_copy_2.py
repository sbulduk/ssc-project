# from services.ad.ad_credentials import ADCredentials
# from ldap3 import Server,Connection,ALL,SUBTREE
# from flask import jsonify
# import subprocess

# class AD(object):
# 	def __init__(self):
# 		self.ldapServer,self.ladpUser,self.ladpPassword,self.searchBase=ADCredentials.GetCredentials()

# 	def Connection(self):
# 		try:
# 			adServer=Server(self.ldapServer,get_info=ALL)
# 			adConn=Connection(adServer,user=self.ladpUser,password=self.ladpPassword,auto_bind=True)
# 			print(str(type(adConn)))
# 			return adConn
# 		except Exception as e:
# 			return jsonify({"success":False,"data":f"Error while connecting to AD server.\nError details: {e}"})

# 	def GetAllGroups(self):
# 		try:
# 			with self.Connection() as conn:
# 				conn.search(search_base=self.searchBase,search_filter="(objectClass=group)",search_scope=SUBTREE)
# 				groupList=[entry.entry_dn for entry in conn.entries]
# 				if len(groupList)==0:
# 					return jsonify({"success":True,"data":f"No groups found in the AD server."})
# 				return jsonify({"success":True,"data":groupList})
# 		except Exception as e:
# 			return jsonify({"success":False,"data":f"Error while loading groups.\nError details: {e}"})

# 	def AddNewGroup(self,groupName,groupDescription=None):
# 		pass
		
# 	def UpdateGroup(self,groupName,newName,newDescription):
# 		pass

# 	def DeleteGroup(self,groupName):
# 		pass
		
# 	def GetUsersByGroup(self,groupName):
# 		try:
# 			with self.Connection() as conn:
# 				conn.search(search_base="DC=example,DC=com",search_filter=f"(objectClass=user)(memberOf={groupName})",search_scope=SUBTREE)
# 				userList=[entry.entry_dn for entry in conn.entries]
# 				if userList.count()==0:
# 					return jsonify({"success":True,"data":f"No users found in the group {groupName}"})
# 				return jsonify({"success":True,"data":userList})
# 		except Exception as e:
# 			return jsonify({"success":False,"data":f"Error while loading the users in the group {groupName}.\nError details: {e}"})

# 	def AddNewUser(self,group,user):
# 		pass

# 	def UpdateUser(self,groupName,userName):
# 		pass