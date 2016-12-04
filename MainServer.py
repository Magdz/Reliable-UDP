"""
Main logic for running the server goes here.
"""

import sys
import socket
import cPickle as pickle
import os
from Server import Server
from SenderHelper import SenderHelper
from DataPacket import DataPacket
from AckPacket import AckPacket
from Datagram import Datagram

myIp = '127.0.0.1'
myPort = 8888
seqNo = 0
ackNo = 0
checkSum = 0

# Starting Server
server = Server(myIp, myPort)
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

# INFO = recvRequest[1].split('\n')
REQUESTS = recvRequest[0].split('\n')

ip = recvRequest[1][0]
filename = REQUESTS[3]

print "Received a request for " + str(filename)
port = recvRequest[1][1]
print "Request is received from IP: " + str(ip) + " from Port: " + str(port)

# Check of file existance and send response
if(SenderHelper.fileExists(filename)):
	sendResponse = "200 OK"
else:
	sendResponse = "404 Not Found"
server.connection.sendto(sendResponse, (myIp, port))
print "Sending Response: " + sendResponse


# Split the file into chunks
chunks = SenderHelper.createChunks(filename)
print "Chunks Created"
server.connection.sendto(str(len(chunks)), (myIp, port))
print "Size of chunks is: "  + str(sys.getsizeof(chunks))
print "Length of chunks is: " + str(len(chunks))

# Start Processing
#index = 0
for chunk in chunks:
	print "\n"
	sendPacket = DataPacket(chunk, seqNo, checkSum)
	sendGram = Datagram(myIp, myPort, ip, port, sendPacket)
	sendMsg = pickle.dumps(sendGram, -1)
	ackNo = seqNo
	while True:
		sendGram.setProbability()
		if not sendGram.isLost():
			server.connection.sendto(sendMsg, (sendGram.ipTo, sendGram.portTo))
		print "Sending Packet #" + str(seqNo)
		print "Timer Started"
		seqNo = ackNo
		# start timer
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
