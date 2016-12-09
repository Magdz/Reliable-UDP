import sys
import random

class Datagram:
	ipFrom = None
	portFrom = None
	ipTo = None
	portTo = None
	packet = None
	__PLP = None
	__Probability = 0.1	# Higher Probability means Higher losses rate

	def __init__(self, ipFrom, portFrom, ipTo, portTo, packet):
		self.ipFrom = ipFrom
		self.portFrom = portFrom
		self.ipTo = ipTo
		self.portTo = portTo
		self.packet = packet
		self.setProbability()

	def setProbability(self):
		self.__PLP = int(random.uniform(0, 1) + self.__Probability)

	def isLost(self):
		return self.__PLP