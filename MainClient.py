"""
Main logic for running the client goes here.
"""
import sys
from Client import Client

#Client Input
SERVERNAME = '127.0.0.1'
PORT = 8888
FILENAME = 'nature.jpg'

#Create Socket Connection
CLIENT = Client(SERVERNAME, PORT)
CLIENTSOCKET = CLIENT.get_connection()

#Send file request to Server
REQUEST = open('request.txt', "rb")
REQUEST_MSG = REQUEST.read()
CLIENTSOCKET.sendto(FILENAME, (SERVERNAME, PORT))

SEQNO = 0

#Receive Response from Server
RESPONSE = CLIENTSOCKET.recvfrom(1024)
print RESPONSE[0]
print CLIENT
print CLIENTSOCKET
print type(CLIENT)
print type(CLIENTSOCKET)

CLIENT.close_socket()
print CLIENTSOCKET

"""while (CLIENTSOCKET)
{

}
"""
sys.exit()
