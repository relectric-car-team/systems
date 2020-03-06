from net import NetData, PiNet
import socket
import json
import logging

# Simple file for testing the net library as a client

logging.basicConfig(level=logging.INFO)
print(socket.gethostname())
clientNet = PiNet(False, ("127.0.0.1", 25500))
data = []
for i in range(0, 20):
	data.append(NetData("Integer" + str(i*5), i*5))
	clientNet.registerNetDataObj(data[i])
clientNet.start()
while True:
	command = input().split()
	if len(command) > 0:
		if command[0] == "poseQuery":
			print(clientNet.poseQuery(command[1:]))
		elif command[0] == "getResponse":
			print(clientNet.getResponse(int(command[1])))
		elif command[0] == "exit":
			break
clientNet.stop()
clientNet = None
exit()