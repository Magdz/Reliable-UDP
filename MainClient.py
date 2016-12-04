"""
Main logic for running the client goes here.
"""
import sys
import cPickle as pickle
import socket
from Client import Client
from DataPacket import DataPacket
from ReceiverHelper import ReceiverHelper

#Connection Details and Function Params
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
CHUNKS = []

#Receive Response from Server with file size
RESPONSE = CLIENTSOCKET.recvfrom(1024)
LENGTH = RESPONSE[0]
print "Expected length of Packet: " + LENGTH
INIT_LEN = 0

while INIT_LEN < int(LENGTH):
    #print INIT_LEN
    #print float(LENGTH)
    ReceiverHelper.update_progress(INIT_LEN/float(LENGTH))
    #print "\n"
    #Receives data packet from the client
    #print "Expecting Packet " + str(SEQNO)
    DATA_PICKLE = CLIENTSOCKET.recvfrom(1024)

    #Extracts pickle to packet
    DATA_PCK = pickle.loads(DATA_PICKLE[0]).packet
    #print "Received Packet " + str(DATA_PCK.seqNo)

    if (isinstance(DATA_PCK, DataPacket) and DATA_PCK.seqNo == SEQNO and
            ReceiverHelper.isCorrupt(DATA_PCK.chunk, DATA_PCK.checkSum)):
        #Append chunk to chunks
        #print "Chunk added to List"
        #print "size of chunk is: " + str(sys.getsizeof(DATA_PCK.chunk))
        CHUNKS.append(DATA_PCK.chunk)

        #Let the ACKNO signal the same sequence number that has been received
        ACKNO = SEQNO

        #Change expected sequence number of next packet
        SEQNO = 1 - SEQNO
        #print "Expected SEQNO is " + str(SEQNO)

        #Send ACK to server and confirm that expected packet sequence number has been received
        CLIENT.udt_send_ack(ACKNO, '127.0.0.1', 8888)
        INIT_LEN += 1
       # print "Current Size of Data is " + str(sys.getsizeof(CHUNKS))

    else:#isinstance(DATA_PCK, DataPacket) and DATA_PCK.seqNo != SEQNO
        #Resend ACK to server
        #print "Client did not receive expected SeqNo."
        #print "Expected SeqNo is: " + str(SEQNO)
        #print "Received SeqNo is: " + str(DATA_PCK.seqNo)
        CLIENT.udt_send_ack(ACKNO, '127.0.0.1', 8888)
    #print "\n"

ReceiverHelper.update_progress(INIT_LEN/float(LENGTH))
#CREATE FILE FROM CHUNKS
print "Total Chunks Received is: " + str(sys.getsizeof(CHUNKS))
print "Total Length of Chunk is: " + str(len(CHUNKS))
ReceiverHelper.create_file('NewFile.jpg', CHUNKS)
sys.exit()
