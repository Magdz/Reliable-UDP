import hashlib
import cPickle as pickle
import sys
import socket
from AckPacket import AckPacket
from DataPacket import DataPacket
from Datagram import Datagram
from Helper import Helper
from Chunk import Chunk

class SenderHelper(Helper):
    """ Contains all methods sender needs to perform its logic"""
    @staticmethod
    def file_exists(filename):
        """Checks if called file exists and if it does, returns an instance of it"""
        try:
            openfile = open(filename, 'rb')
            return openfile
        except Exception, e:
            return False

    @staticmethod
    def create_chunks(filename):
        """Creates an array of chunks from the file specified"""
        chunks = []
        rcvfile = SenderHelper.file_exists(filename)
        if rcvfile:
            while True:
                data = rcvfile.read(500)
                if not data:
                    break
                chunk = Chunk(data)
                chunks.append(chunk)
        return chunks

    @staticmethod
    def is_corrupt(chunk, checksum):
        """Check if the chunk is corrupt or not"""
        return str(hashlib.md5(chunk.getData()).hexdigest()) == checksum

    @staticmethod
    def fetch_request(recvrequest):
        """Returns the requested parameters for server logic"""
        requests = recvrequest[0].split('\n')
        hostname = recvrequest[1][0]
        filename = requests[3]
        port = recvrequest[1][1]
        return hostname, filename, port

    @staticmethod
    def make_packet(chunk, seqno, hostname, port, ipnumnum):
        """Make packet to be sent to client"""
        sendpacket = DataPacket(chunk, seqno)
        sendgram = Datagram(hostname, port, ipnumnum, port, sendpacket)
        sendmsg = pickle.dumps(sendgram, -1)
        return sendmsg, sendgram

    @staticmethod
    def recv_packet(recvmsg):
        """Receive Ack packet from client"""
        recvpacket = pickle.loads(recvmsg[0])
        return recvpacket

    @staticmethod
    def execute_request(recvrequest, server, hostname):
        """Execute get request for each client"""
        seqno = 0
        ackno = 0

        #Fetch Requests variables
        ipnum, filename, port = SenderHelper.fetch_request(recvrequest)
        #Print Information given from Client
        print "Received a request for " + str(filename)
        print "Request is received from ipnum: " + str(ipnum) + " from port: " + str(port)

        # Check if file exists
        if SenderHelper.file_exists(filename):
            sendresponse = "200 OK"
        else:
            sendresponse = "404 Not Found"
        # Send found/not found response to client
        server.connection.sendto(sendresponse, (hostname, port))
        print "Sending Response: " + sendresponse

        # Split the file into chunks
        chunks = SenderHelper.create_chunks(filename)
        print "chunks Created"
        # Send file information to client
        server.connection.sendto(str(len(chunks)), (hostname, port))
        print "Size of chunks is: "  + str(sys.getsizeof(chunks))
        print "Length of chunks is: " + str(len(chunks))

        # Start Processing get request
        for chunk in chunks:
            #Make packet
            print "\n"
            sendmsg, sendgram = SenderHelper.make_packet(chunk, seqno, hostname, port, ipnum)
            ackno = seqno

            while True:
                #sendgram.setprobability() #Set loss probability

                #Send Packet to client
                if not sendgram.isLost():
                    server.connection.sendto(sendmsg, (sendgram.ip_to, sendgram.port_to))
                print "Sending Packet #" + str(seqno)
                print "Timer Started"
                seqno = ackno

                #Wait for ACK from client
                print "Waiting for Ack #" + str(ackno)
                try:
                    recvmsg = server.connection.recvfrom(1024)
                except socket.timeout:
                    print "Timeout"
                    continue

                #Receive ACK Packet from client
                recvpacket = SenderHelper.recv_packet(recvmsg)

                if isinstance(recvpacket, AckPacket):
                    print "Received Ack #" + str(recvpacket.ackNo)
                    if recvpacket.ackNo == ackno:
                        seqno = 1 - seqno
                        # Stop timer
                        print "Timer Stopped"
                        break
                    else:
                        print "Unexpected Ack"
                        # Stop timer
                        print "Timer Stopped"
                        print "Resending Packet #" + str(seqno)
                else:
                    print "Received a corrupted packet"
                    # Stop timer
                    print "Timer Stopped"
                    print "Resending Packet #" + str(seqno)
                print "\n"
        print "All Packets are sent successfully"
