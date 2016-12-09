import sys
from Packet import Packet

class DataPacket(Packet):
	seqNo = None
	chunk = None

	def __init__(self, chunk, seqNo, checkSum):
		self.seqNo = seqNo
		self.chunk = chunk
		length = len(chunk.getData()) + 8
		super(DataPacket, self).__init__(length, checkSum)