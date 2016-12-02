import sys

class Datagram:
	ip = None
	port = None
	packet = None

	def __init__(self, ip, port, packet):
		self.ip = ip
		self.port = port
		self.packet = packet