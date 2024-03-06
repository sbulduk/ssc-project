from .vm_credentials import VMCredentials
from pyvim import connect
import ssl
from pyVmomi import vmodl,vim

class VM():
	def __init__(self):
		try:
			self.context=ssl.SSLContext(ssl.PROTOCOL_SSLv23)
			self.context.verify_mode=ssl.CERT_NONE
			self.host,self.username,self.password=VMCredentials.GetCredentials()
			self.vmServiceInstance=None
			self.virtualMachineList=[]
		except Exception as e:
			print(f"Could not establish connection. Error: {e}")
	
	def Connect(self):
		if self.vmServiceInstance is None:
			try:
				self.vmServiceInstance=connect.SmartConnect(
					host=self.host,
					user=self.username,
					pwd=self.password,
					sslContext=self.context,
					port=443
				)
				print("ESXi Connection Established Successfully!")
			except vmodl.MethodFault as e:
				print(f"vmodl fault: {e.msg}\nError while connecting to the server: {e}")
				return None
		return self.vmServiceInstance
		
	def GetVirtualMachineList(self,serviceInstance):
		if serviceInstance:
			content=serviceInstance.RetrieveContent()
			container=content.rootFolder
			viewType=[vim.VirtualMachine]
			recursive=True
			containerView=content.viewManager.CreateContainerView(container,viewType,recursive)
			children=containerView.view
			
			for child in children:
				self.virtualMachineList.append(child)
			return self.virtualMachineList
		else:
			return {"success":False,"body":"Instance could not be found!"}

	def GetVirtualMachineById(self,id):
		try:
			for virtualMachine in self.virtualMachineList:
				if virtualMachine.id==id:
					return virtualMachine
		except Exception as e:
			return {"success":False,"body":"The ID: {id} is not a valid Virtual Machine: {e}"}

	def ShowStatus(self,virtualMachine):
		if not virtualMachine:
			print("VM not selected")
		else:
			print(f"Status: {virtualMachine.runtime.powerState}")
	
	def PowerOn(self,virtualMachine):
		if not virtualMachine:
			print("VM not selected")
		else:
			if virtualMachine.runtime.powerState==vim.VirtualMachinePowerState.poweredOff:
				print(f"Powering On VM: {virtualMachine.id}")
				virtualMachine.PowerOn()
			else:
				print(f"{virtualMachine.name} is already powered on.")
	
	def PowerOff(self,virtualMachine):
		if not virtualMachine:
			print("VM not selected")
		else:
			if virtualMachine.runtime.powerState==vim.VirtualMachinePowerState.poweredOn:
				print(f"Powering Off VM: {virtualMachine.name}")
				virtualMachine.PowerOff()
			else:
				print(f"{virtualMachine.name} is not powered on.")

	def Restart(self,virtualMachine):
		if not virtualMachine:
			print("VM not selected")
		else:
			print(f"Restarting: {virtualMachine.name}")
			self.PowerOff(virtualMachine)
			self.PowerOn(virtualMachine)
	
	def CloseConnection(self,serviceInstance):
		if serviceInstance:
			connect.Disconnect(serviceInstance)
			serviceInstance=None

	def __del__(self):
		if hasattr(self,"vmServiceInstance") and self.vmServiceInstance is not None:
			self.CloseConnection(self.vmServiceInstance)