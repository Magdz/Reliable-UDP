# the main logic for running the server goes here.

import sys
from Server import Server
from SenderHelper import SenderHelper
from DataPacket import DataPacket

if(SenderHelper.fileExists("Server.py")):
	chunks = SenderHelper.createChunks("Server.py")
	for chunk in chunks:
		print chunk.getData()
		dataPacket = DataPacket(chunk, 0, 0)
else:
	print "No"