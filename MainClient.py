"""
Main logic for running the client goes here.
"""
import sys
import cPickle as pickle
import socket
from Client import Client
from Datagram import Datagram
from DataPacket import DataPacket
from AckPacket import AckPacket

REQUEST = open('request.txt', "rb")
INPUT = REQUEST.read()
INPUT_LIST = INPUT.split('\n')
SERVERNAME = INPUT_LIST[0]
PORT = INPUT_LIST[1]

#Create Socket Connection
CLIENT = Client(SERVERNAME, PORT)
CLIENTSOCKET = CLIENT.get_connection()
#try:
CLIENTSOCKET.sendto(INPUT, ('127.0.0.1', 8888))
print 'Send Request Sent'
"""
except socket.error:
    print 'Error establishing a connection to send request'
    print 'Server not found'
    sys.exit()
"""
#initial expected sequence  and ACK number
SEQNO = 0
ACKNO = 0


#Receive Response from Server
RESPONSE = CLIENTSOCKET.recvfrom(1024)
print RESPONSE[0]
CHUNKS = []
NEXTPACKET = True

while NEXTPACKET:
    RECVPCK = CLIENTSOCKET.recvfrom(1024)
    RECGRM = pickle.loads(RECVPCK[0])
    NEXTPACKET = False
    RECPCKT = RECGRM.packet
    if isinstance(RECPCKT, DataPacket) and RECPCKT.seqNo == SEQNO:
        #Append chunk to chunks
        CHUNKS.append(RECPCKT.chunk)
        ACKNO = SEQNO
        ACK_MSG = AckPacket(ACKNO, None)
        ACK_SEND = pickle.dumps(ACK_MSG, -1)
        #Send ACK to server
        CLIENTSOCKET.sendto(ACK_SEND, ('127.0.0.1', 8888))
sys.exit()
