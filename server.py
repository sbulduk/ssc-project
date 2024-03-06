from base.app_config import AppConfig
from flask_cors import CORS

class Server(object):
	def __init__(self):
		self.app=AppConfig.RunApp()
		CORS(self.app,origins=["http://localhost:5000"])

	def Start(self):
		self.app.run(debug=True)

if __name__=="__main__":
	server=Server()
	server.Start()