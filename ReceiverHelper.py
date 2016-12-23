import sys
import hashlib
from Helper import Helper

class ReceiverHelper(Helper):

	@staticmethod
	def create_file(fileName, chunks):
		file = open(fileName, 'ab+')
		for chunk in chunks:
			file.write(chunk.getData())
	@staticmethod
	def update_progress(progress):
		barLength = 50 # Modify this to change the length of the progress bar
		status = ""
		if isinstance(progress, int):
			progress = float(progress)
		if not isinstance(progress, float):
			progress = 0
			status = "error: progress var must be float\r\n"
		if progress < 0:
			progress = 0
			status = "Halt...\r\n"
		if progress >= 1:
			progress = 1
			status = "Done...\r\n"
		block = int(round(barLength*progress))
		text = "\rPercent: [{0}] {1:.2f}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
		sys.stdout.write(text)
		sys.stdout.flush()
	@staticmethod
	def isCorrupt(chunk, checksum):
		return str(hashlib.md5(chunk.getData()).hexdigest()) == checksum
