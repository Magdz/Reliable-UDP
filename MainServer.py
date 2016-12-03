# the main logic for running the server goes here.

import sys
from Server import Server
from SenderHelper import SenderHelper
from DataPacket import DataPacket
from AckPacket import AckPacket
from Datagram import Datagram
import cPickle as pickle

myIp = '127.0.0.1'
myPort = 80
seqNo = 0
ackNo = 0
checkSum = 0

# Starting Server
server = Server(myIp, myPort)
print "Server Started"

# Waiting until a Request is received
recvRequest = server.connection.recvfrom(1024)
fileName = recvRequest[0]
print "Received a request for " + str(fileName)
ip = recvRequest[0][0]
port = recvRequest[0][1]
print "Request is received from IP: " + str(ip) + " from Port: " + str(port)

# Check of file existance and send response
if(SenderHelper.fileExists(fileName)):
	sendResponse = "200 OK"
else:
	sendResponse = "404 Not Found"
server.connection.sendto(sendResponse, (myIp, myPort))
print sendResponse

# Split the file into chunks
chunks = SenderHelper.createChunks(fileName)
print "Chunks Created"

# Start Processing
for index, chunk in chunks:
	sendPacket = DataPacket(chunk, seqNo, checkSum)
	sendGram = Datagram(myIp, myPort, ip, port, sendPacket)
	sendMsg = pickle.dumps(sendGram, -1)
	ackNo = seqNo
	while True:
		server.connection.sendto(sendMsg, (sendGram.ipTo, sendGram.portTo))
		print "Sending Packet #" + str(index)
		print "Timer Started"
		# start timer
		print "Waiting for Ack #" + str(index)
		recvMsg = server.connection.recvfrom(1024)
		recvGram = pickle.loads(recvMsg[0])
		recvPacket = recvGram.packet
		if(type(recvPacket) is AckPacket):
			print "Received Ack #" + str(recvPacket.ackNo)
			if(recvPacket.ackNo == ackNo):
				seqNo = (seqNo & 1) % 2
				# stop timer
				print "Timer Stopped"
				break
			else:
				print "Unexpected Ack"
				# stop timer
				print "Timer Stopped"
				print "Resending Packet #" + str(index)
		else:
			print "Received a corrupted packet"
			# stop timer
			print "Timer Stopped"
			print "Resending Packet #" + str(index)
			
print "All Packets are sent successfully"
print "Closing the server"
