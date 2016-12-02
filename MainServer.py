# the main logic for running the server goes here.

import sys
from Server import Server
from SenderHelper import SenderHelper
from ReceiverHelper import ReceiverHelper
from DataPacket import DataPacket
from AckPacket import AckPacket

if(SenderHelper.fileExists("Server.py")):
	chunks = SenderHelper.createChunks("Server.py")
	ReceiverHelper.createFile("Server.py", chunks)
else:
	print "No"