"""
Main logic for running the server goes here.
"""

import sys
import socket
import cPickle as pickle
from Server import Server
from AckPacket import AckPacket

SERVERIP = '127.0.0.1'
SERVERPORT = 8888

seqNo = 0
ackNo = 0
checkSum = 0

# Starting Server
server = Server(SERVERIP, SERVERPORT)
print "Server Started"

# Waiting until a Request is received
"""

"""
WAITTOCONNECT = True
while WAITTOCONNECT:
	try:
		recvRequest = server.connection.recvfrom(1024)
		WAITTOCONNECT = False	
	except socket.timeout:
		pass

server.receiveRequest(recvRequest)

# Check of file existance and send response
server.sendResponse()

# Split the file into chunks
chunks = server.createChunks()

# Start Processing
#index = 0
server.processChunks(chunks)
