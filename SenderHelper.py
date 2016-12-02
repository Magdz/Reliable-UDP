import sys
from Helper import Helper
from Chunk import Chunk

class SenderHelper(Helper):

	@staticmethod
	def fileExists(fileName):
		try:
			file = open(fileName, 'r')
			return True
		except Exception, e:
			return False

	@staticmethod
	def createChunks(self, fileName):
		chunks = []
		if(self.fileExists(fileName)):
			while True:
				data = file.readline(512)
				if not data:
					break
				chunk = Chunk(data)
				chunks.append(chunk)
		return chunks