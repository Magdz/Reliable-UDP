import sys

class Chunk:
	data = []

	def __init__(self, data):
		self.data = data

	def setData(self, data):
		self.data = data

	def getData(self):
		return self.data