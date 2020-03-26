from net import NetData, PiNet
import socket
import json
import logging

# Simple file for testing the net library as a server

logging.basicConfig(level=logging.INFO)
print(socket.gethostname())
serverNet = PiNet(True, ("127.0.0.1", 25500))
data = []
for i in range(0, 20):
	data.append(NetData("Integer" + str(i), i))
	serverNet.registerNetDataObj(data[i])
serverNet.start()
while True:
	command = input().split()
	if len(command) > 0:
		if command[0] == "poseQuery":
			print(serverNet.poseQuery(command[2:], int(command[1])))
		elif command[0] == "getResponse":
			print(serverNet.getResponse(int(command[1])))
		elif command[0] == "getConnected":
			print(serverNet.getConnected())
		elif command[0] == "exit":
			break
serverNet.stop()
serverNet = None
exit()