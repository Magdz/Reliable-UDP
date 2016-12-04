import sys
from Helper import Helper
from Chunk import Chunk

class SenderHelper(Helper):

	@staticmethod
	def fileExists(fileName):
		try:
			file = open(fileName, 'rb')
			return file
		except Exception, e:
			return False

	@staticmethod
	def createChunks(fileName):
		chunks = []
		file = SenderHelper.fileExists(fileName)
		if(file):
			while True:
				data = file.read(500)
				if not data:
					break
				chunk = Chunk(data)
				chunks.append(chunk)
		return chunks