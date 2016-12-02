# the main logic for running the server goes here.

import sys
from Server import Server
from SenderHelper import SenderHelper

if(SenderHelper.fileExists("Server.py")):
	chunks = SenderHelper.createChunks("Server.py")
	for chunk in chunks:
		print chunk.getData()
else:
	print "No"