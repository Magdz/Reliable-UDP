import sys
from Helper import Helper

class ReceiverHelper(Helper):

	@staticmethod
	def create_file(fileName, chunks):
		file = open(fileName, 'a')
		for chunk in chunks:
			file.write(chunk.getData())
