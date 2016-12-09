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
THREADS = []

# Starting Server
server = Server(SERVERIP, SERVERPORT)
print "Server Started"

# Waiting until a Request is received
"""

"""
WAITTOCONNECT = True
while WAITTOCONNECT:
	try:
		REQUEST = server.connection.recvfrom(1024)
		server.handleThread(REQUEST)
		sys.exit()
	except socket.timeout:
		pass

