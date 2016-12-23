# here goes the properties and the functions of the Server as an Object

import sys
import socket
import cPickle as pickle
from SenderHelper import SenderHelper
from DataPacket import DataPacket
from AckPacket import AckPacket
from Datagram import Datagram

class Server:
	SERVERIP = None
	SERVERPORT = None
	connection = None

	FILENAME = None
	CLIENTIP = None
	CLIENTPORT = None
	SEQNO = 0
	ACKNO = 0
	CHECKSUM = 0

	def __init__(self, SERVERIP, SERVERPORT):
		try:
			# UDP Socket Connection
			self.SERVERIP = SERVERIP
			self.SERVERPORT = SERVERPORT
			self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.connection.settimeout(1)
			self.connection.bind((self.SERVERIP, self.SERVERPORT))
			print "Server socket connection initialized"
		except Exception, e:
			print "Server socket connection failed: " + str(e)
			sys.exit()

	def handleThread(self, REQUEST):
		self.receiveRequest(REQUEST)
		self.sendResponse()

		if not SenderHelper.fileExists(self.FILENAME):
			sys.exit()
		# Split the file into chunks
		chunks = self.createChunks()
		# Start Processing
		self.processChunks(chunks)

	def receiveRequest(self, REQUEST):
		print REQUEST
		self.FILENAME = REQUEST[0]
		self.CLIENTIP = REQUEST[1][0]
		self.CLIENTPORT = REQUEST[1][1]
		
		print "Received a request for " + str(self.FILENAME)
		print "Request is received from IP: " + str(self.CLIENTIP) + " from Port: " + str(self.CLIENTPORT)
		return self.FILENAME

	def sendResponse(self):
		if(SenderHelper.fileExists(self.FILENAME)):
			RESPONSE = "200 OK"
		else:
			RESPONSE = "404 Not Found"
		self.connection.sendto(RESPONSE, (self.SERVERIP, self.CLIENTPORT))
		print "Sending Response: " + RESPONSE

	def createChunks(self):
		chunks = SenderHelper.createChunks(self.FILENAME)
		print "Chunks Created"
		self.connection.sendto(str(len(chunks)), (self.SERVERIP, self.CLIENTPORT))
		print "Size of chunks is: "  + str(sys.getsizeof(chunks))
		print "Length of chunks is: " + str(len(chunks))
		return chunks

	def sendData(self, chunk):
		PACKET = DataPacket(chunk, self.SEQNO, self.CHECKSUM)
		DATAGRAM = Datagram(self.SERVERIP, self.SERVERPORT, self.CLIENTIP, self.CLIENTPORT, PACKET)
		MSG = pickle.dumps(DATAGRAM, -1)
		self.ACKNO = self.SEQNO
		DATAGRAM.setProbability()
		if not DATAGRAM.isLost():
			self.connection.sendto(MSG, (DATAGRAM.ipTo, DATAGRAM.portTo))
		print "Sending Packet #" + str(self.SEQNO)
		print "Timer Started"

	def processChunks(self, chunks):
		for chunk in chunks:
			print "\n"
			while True:
				self.sendData(chunk)
				print "Waiting for Ack #" + str(self.ACKNO)
				try:
					recvMsg = self.connection.recvfrom(1024)
				except socket.timeout:
					print "Timeout"
					continue
				recvGram = pickle.loads(recvMsg[0])
				recvPacket = recvGram #.packet
				if(type(recvPacket) is AckPacket):
					print "Received Ack #" + str(recvPacket.ackNo)
					if(recvPacket.ackNo == self.ACKNO):
						self.SEQNO = 1 - self.SEQNO
						# stop timer
						print "Timer Stopped"
						break
					else:
						print "Unexpected Ack"
						# stop timer
						print "Timer Stopped"
						print "Resending Packet #" + str(self.SEQNO)
				else:
					print "Received a corrupted packet"
					# stop timer
					print "Timer Stopped"
					print "Resending Packet #" + str(self.SEQNO)
				print "\n"
		print "All Packets are sent successfully"
		print "Closing the server"