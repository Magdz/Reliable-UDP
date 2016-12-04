"""
Main logic for running the SERVER goes here.
"""

import sys
import socket
import cPickle as pickle
from Server import Server
from SenderHelper import SenderHelper
from DataPacket import DataPacket
from AckPacket import AckPacket
from Datagram import Datagram

#Connection Details and Function Params
HOSTNAME = '127.0.0.1'
PORT = 8888
SEQNO = 0
ACKNO = 0
CHECKSUM = 0

# Starting SERVER
SERVER = Server(HOSTNAME, PORT)
print "SERVER Started"

# Waiting until a Request is received
WAITTOCONNECT = True
while WAITTOCONNECT:
    try:
        RECVREQUEST = SERVER.connection.recvfrom(1024)
        WAITTOCONNECT = False
    except socket.timeout:
        pass

#Fetch Requests variables
REQUESTS = RECVREQUEST[0].split('\n')
IP = RECVREQUEST[1][0]
FILENAME = REQUESTS[3]
PORT = RECVREQUEST[1][1]

#Print Information given from Client
print "Received a request for " + str(FILENAME)
print "Request is received from IP: " + str(IP) + " from PORT: " + str(PORT)

# Check if file exists and send response
if SenderHelper.fileExists(FILENAME):
    SENDRESPONSE = "200 OK"
else:
    SENDRESPONSE = "404 Not Found"
SERVER.connection.sendto(SENDRESPONSE, (HOSTNAME, PORT))
print "Sending Response: " + SENDRESPONSE


# Split the file into CHUNKS
CHUNKS = SenderHelper.createChunks(FILENAME)
print "CHUNKS Created"
SERVER.connection.sendto(str(len(CHUNKS)), (HOSTNAME, PORT))
print "Size of CHUNKS is: "  + str(sys.getsizeof(CHUNKS))
print "Length of CHUNKS is: " + str(len(CHUNKS))

# Start Processing
for chunk in CHUNKS:
    print "\n"
    sendPacket = DataPacket(chunk, SEQNO)
    sendGram = Datagram(HOSTNAME, PORT, IP, PORT, sendPacket)
    sendMsg = pickle.dumps(sendGram, -1)
    ACKNO = SEQNO
	#
    while True:
        sendGram.setprobability()
        if not sendGram.isLost():
            SERVER.connection.sendto(sendMsg, (sendGram.ip_to, sendGram.port_to))
        print "Sending Packet #" + str(SEQNO)
        print "Timer Started"
        SEQNO = ACKNO

		# Start timer
        print "Waiting for Ack #" + str(ACKNO)
        try:
            recvMsg = SERVER.connection.recvfrom(1024)
        except socket.timeout:
            print "Timeout"
            continue
        recvGram = pickle.loads(recvMsg[0])
        recvPacket = recvGram
        if isinstance(recvPacket, AckPacket):
            print "Received Ack #" + str(recvPacket.ackNo)
            if recvPacket.ackNo == ACKNO:
                SEQNO = 1 - SEQNO
				# Stop timer
                print "Timer Stopped"
                break
            else:
                print "Unexpected Ack"
        		# Stop timer
                print "Timer Stopped"
                print "Resending Packet #" + str(SEQNO)
        else:
            print "Received a corrupted packet"
			# Stop timer
            print "Timer Stopped"
            print "Resending Packet #" + str(SEQNO)
        print "\n"

print "All Packets are sent successfully"
print "Closing the SERVER"
