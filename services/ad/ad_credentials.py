class ADCredentials(object):
	_host="WS19DC.TASLOG.local"
	_user="sbulduk"
	_password="Sbulduk2024!"
	_searchBase="DC=TASLOG,DC=local"

	@staticmethod
	def GetCredentials():
		return ADCredentials._host,ADCredentials._user,ADCredentials._password,ADCredentials._searchBase