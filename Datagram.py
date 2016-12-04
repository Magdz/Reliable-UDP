import sys

class Datagram:
	ipFrom = None
	portFrom = None
	ipTo = None
	portTo = None
	packet = None
	PLP = None

	def __init__(self, ipFrom, portFrom, ipTo, portTo, packet):
		self.ipFrom = ipFrom
		self.portFrom = portFrom
		self.ipTo = ipTo
		self.portTo = portTo
		self.packet = packet