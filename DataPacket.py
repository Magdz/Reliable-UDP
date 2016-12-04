import sys
import hashlib
from Packet import Packet

class DataPacket(Packet):
	seqNo = None
	chunk = None

	def __init__(self, chunk, seqNo):
		self.seqNo = seqNo
		self.chunk = chunk
		length = len(chunk.getData()) + 8
		checkSum = str(hashlib.md5(self.chunk.getData()).hexdigest())
		super(DataPacket, self).__init__(length, checkSum)

	def getChecksum(self):
		return self.checkSum