import sys

class Packet(object):
	checkSum = None
	length = None

	def __init__(self, length, checkSum):
		self.checkSum = checkSum
		self.length = length