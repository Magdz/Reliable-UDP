# here goes the properties and the functions of the Server as an Object

import socket
import sys

class Server:
	ip = None
	port = None
	connection = None

	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.initializeSocket()

	def initializeSocket(self):
		try:
			# UDP Socket Connection
			self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.connection.bind((self.ip, self.port))
			print "Server socket connection initialized"
		except Exception, e:
			print "Server socket connection faild: " + str(e)
			sys.exit()