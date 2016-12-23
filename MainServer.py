"""
Main logic for running the server goes here.
"""

import sys
import socket
from threading import Thread
from random import randrange
from Server import Server
from SenderHelper import SenderHelper

SERVERIP = '127.0.0.1'
SERVERPORT = 8888
THREADS = []

# Starting Server
server = Server(SERVERIP, SERVERPORT)
print "Server Started"

# Waiting until a Request is received
"""

"""
REQUEST = None
while not REQUEST:
	try:
		REQUEST = server.connection.recvfrom(1024)
		print "Request Received"
		THREAD = Server(SERVERIP, randrange(2000, 8000))
		THREADS.append(THREAD)
		print "Thread Created"
		Thread(target=THREAD.handleThread, args=[REQUEST]).start()
		REQUEST = None
	except socket.timeout:
		pass
