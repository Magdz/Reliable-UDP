import sys
from Packet import Packet

class AckPacket(Packet):
	ackNo = None

	def __init__(self, ackNo, checkSum):
		self.ackNo = ackNo
		length = 8
		super(AckPacket, self).__init__(length, checkSum)