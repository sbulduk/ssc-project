# from .credentials import Credentials
# from pyvim import connect
# import ssl
# from pyVmomi import vmodl,vim

# class VM():
# 	def __init__(self):
# 		context=ssl.SSLContext(ssl.PROTOCOL_SSLv23)
# 		context.verify_mode=ssl.CERT_NONE
# 		self.host,self.username,self.password=Credentials.GetCredentials()
# 		self.vmServiceInstance=connect.SmartConnect(host=self.host,user=self.username,pwd=self.password,sslContext=context)
	
# 	def Connect(self):
# 		try:
# 			vmServiceInstance=self.vmServiceInstance
# 			print("ESXi Connection Established Successfully!")
# 			return vmServiceInstance
# 		except vmodl.MethodFault as error:
# 			print(f"vmodl fault: {error.msg}")
# 			return None
		
# 	def GetVirtualMachineList(self,serviceInstance):
# 		if serviceInstance!=None:
# 			content=serviceInstance.RetrieveContent()
# 			container=content.rootFolder
# 			viewType=[vim.VirtualMachine]
# 			recursive=True
# 			containerView=content.viewManager.CreateContainerView(container,viewType,recursive)
# 			children=containerView.view

# 			i=1
# 			virtualMachineList=[]
# 			for child in children:
# 				virtualMachineList.append(child)
# 				# virtualMachineList.append([i,child.name,child])
# 			return virtualMachineList
# 		else:
# 			print(f"Virtual Machine Instance couldn't be created...")

# 	def SelectVirtualMachine(self):
# 		virtualMachineList=self.GetVirtualMachineList(self.Connect())

# 		if not virtualMachineList:
# 			print("No VM's found!")
# 			return None
# 		if len(virtualMachineList)==1:
# 			print(f"Only one VM is available: {virtualMachineList[0].name} - ({virtualMachineList[0]}) which is automatically selected!")
# 			return virtualMachineList[0]
		
# 		print(f"Available VM instances:")
# 		for i,virtualMachine in enumerate(virtualMachineList,start=1):
# 			print(f"{i}\t{virtualMachine.name}\t - ({virtualMachine})")

# 		while True:
# 			choice=input(f"Select a VM from (1 to {0})".format(len(virtualMachineList)))
# 			try:
# 				choice=int(choice)
# 				if 1<=choice<=len(virtualMachineList):
# 					return virtualMachineList[choice-1]
# 				else:
# 					print(f"Invalid choice. Please enter a number between 1 and {0}".format(len(virtualMachineList)))
# 			except ValueError:
# 				print("Invalid input. Please try again.")

# 	def ShowStatus(self,virtualMachine):
# 		if not virtualMachine:
# 			print("VM not selected")
# 		else:
# 			print(f"{virtualMachine.name} Status: {virtualMachine.runtime.powerState}")
	
# 	def PowerOn(self,virtualMachine):
# 		if not virtualMachine:
# 			print("VM not selected")
# 		else:
# 			if virtualMachine.runtime.powerState==vim.VirtualMachinePowerState.poweredOff:
# 				print(f"Powering On VM: {virtualMachine.name}")
# 				virtualMachine.PowerOn()
# 			else:
# 				print(f"{virtualMachine.name} is already powered on.")
	
# 	def PowerOff(self,virtualMachine):
# 		if not virtualMachine:
# 			print("VM not selected")
# 		else:
# 			if virtualMachine.runtime.powerState==vim.VirtualMachinePowerState.poweredOn:
# 				print(f"Powering Off VM: {virtualMachine.name}")
# 				virtualMachine.PowerOff()
# 			else:
# 				print(f"{virtualMachine.name} is not powered on.")

# 	def Restart(self,virtualMachine):
# 		if not virtualMachine:
# 			print("VM not selected")
# 		else:
# 			print(f"Restarting: {virtualMachine.name}")
# 			self.PowerOff(virtualMachine)
# 			self.PowerOn(virtualMachine)
	
# 	def CloseConnection(self,serviceInstance):
# 		connect.Disconnect(serviceInstance)

# 	def __del__(self):
# 		self.CloseConnection(self.vmServiceInstance)