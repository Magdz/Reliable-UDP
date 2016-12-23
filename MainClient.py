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
from ReceiverHelper import ReceiverHelper


REQUEST = open('request.txt', "rb")
INPUT = REQUEST.read()
INPUT_LIST = INPUT.split('\n')
SERVERNAME = INPUT_LIST[0]
PORT = INPUT_LIST[1]

#Create Socket Connection
CLIENT = Client(SERVERNAME, PORT)
CLIENTSOCKET = CLIENT.get_connection()
try:
    CLIENTSOCKET.sendto(INPUT, ('127.0.0.1', 8888))
    print 'Send Request Sent'
except socket.error:
    print 'Error establishing a connection to send request'
    print 'Server not found'
    sys.exit()

#Initial expected sequence  and ACK number
SEQNO = 0
ACKNO = 0

#Receive Response from Server if file exists
RESPONSE = CLIENTSOCKET.recvfrom(1024)
print RESPONSE[0]

#Receive Response from Server with file size
RESPONSE = CLIENTSOCKET.recvfrom(1024)
LENGTH = RESPONSE[0]
INIT_LEN = 0

while INIT_LEN < int(LENGTH):
    ReceiverHelper.update_progress(INIT_LEN/float(LENGTH))
    #Receives data packet from the client
    DATA_PICKLE = CLIENTSOCKET.recvfrom(1024)

    #Extracts pickle to packet
    DATA_DTG = pickle.loads(DATA_PICKLE[0])
    DATA_PCK = DATA_DTG.packet
    
    if isinstance(DATA_PCK, DataPacket) and DATA_PCK.seqNo == SEQNO:

        #Append chunk to chunks
        ReceiverHelper.append_file('book2.jpg', DATA_PCK.chunk)
        #Let the ACKNO signal the same sequence number that has been received
        ACKNO = SEQNO

        #Change expected sequence number of next packet
        SEQNO = 1 - SEQNO
    
        #Send ACK to server and confirm that expected packet sequence number has been received
        CLIENT.udt_send_ack(ACKNO, '127.0.0.1', DATA_DTG.portFrom)
        INIT_LEN += 1
    
    else:#isinstance(DATA_PCK, DataPacket) and DATA_PCK.seqNo != SEQNO
        #Resend ACK to server
        CLIENT.udt_send_ack(ACKNO, '127.0.0.1', DATA_DTG.portFrom)

ReceiverHelper.update_progress(INIT_LEN/float(LENGTH))
#CREATE FILE FROM CHUNKS
print "Total Chunks Received is: " + str(sys.getsizeof(CHUNKS))
print "Total Length of Chunk is: " + str(len(CHUNKS))
sys.exit()
