"""
Main logic for running the server goes here.
"""

import sys
import socket
import cPickle as pickle
from Server import Server
from AckPacket import AckPacket

seqNo = 0
ackNo = 0
checkSum = 0

# Starting Server
server = Server()
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
for chunk in chunks:
	print "\n"
	while True:
		server.sendData(chunk)
		print "Waiting for Ack #" + str(ackNo)
		try:
			recvMsg = server.connection.recvfrom(1024)
		except socket.timeout:
			print "Timeout"
			continue
		recvGram = pickle.loads(recvMsg[0])
		recvPacket = recvGram #.packet
		if(type(recvPacket) is AckPacket):
			print "Received Ack #" + str(recvPacket.ackNo)
			if(recvPacket.ackNo == ackNo):
				seqNo = 1 - seqNo
				# stop timer
				print "Timer Stopped"
				break
			else:
				print "Unexpected Ack"
				# stop timer
				print "Timer Stopped"
				print "Resending Packet #" + str(seqNo)
		else:
			print "Received a corrupted packet"
			# stop timer
			print "Timer Stopped"
			print "Resending Packet #" + str(seqNo)
		print "\n"

print "All Packets are sent successfully"
print "Closing the server"
