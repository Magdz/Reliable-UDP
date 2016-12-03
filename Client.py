import socket
import sys

class Client(object):
    """
    Defines the Client properties and methods
    """
    __hostname = None
    __port = None
    __clientsocket = None

    def __init__(self, hostname, port):
        self.__ip = hostname
        self.__port = port
        self.initialize_socket()

    def initialize_socket(self):
        """
        Initialize Client Socket
        """
        try:
            self.__clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print 'Client Socket Created successfully.'
        except socket.error:
            print 'Failed to create a Client Socket'
            sys.exit()
            
    def close_socket(self):
        """
        Close opened socket
        """
        self.__clientsocket.close()
        