import os

class VMCredentials(object):
	_host="127.0.0.1"
	_username=os.environ.get("VMWARE_USERNAME") or "taslog\\sbulduk"
	_password=os.environ.get("VMWARE_PASSWORD") or "Sbulduk2023!"

	@staticmethod
	def GetCredentials():
		# print(f"Host: {Credentials._host}\nUsername: {Credentials._username}\nPassword: {Credentials._password}")
		return VMCredentials._host,VMCredentials._username,VMCredentials._password

	@staticmethod
	def PrintCredentials():
		print(f"{VMCredentials._host}\n{VMCredentials._username}\n{VMCredentials._password}")