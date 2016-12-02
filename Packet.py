import sys

class Packet:
	checkSum = None
	length = None

	def __init__(self, length):
		self.length = length