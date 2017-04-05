import os

def Ping(destination):
	hostname = destination
	response = os.system("ping -c 1 " + hostname)

	#and then check the response...
	if response == 0:
		return True
	else:
	 	return False