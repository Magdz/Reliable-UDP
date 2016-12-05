"""
Main logic for running the SERVER goes here.
"""
import socket
from Server import Server
from SenderHelper import SenderHelper

#Connection Details and Function Params
HOSTNAME = '127.0.0.1'
PORT = 8888
SEQNO = 0
ACKNO = 0
CHECKSUM = 0

# Starting SERVER
SERVER = Server(HOSTNAME, PORT)
print "SERVER Started"

# Waiting until a Request is received
WAITTOCONNECT = True
while WAITTOCONNECT:
    try:
        RECVREQUEST = SERVER.connection.recvfrom(1024)
        WAITTOCONNECT = False
    except socket.timeout:
        pass
SenderHelper.execute_request(RECVREQUEST, SERVER, HOSTNAME)