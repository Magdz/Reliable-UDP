import random

class Datagram(object):
    ip_from = None
    port_from = None
    ip_to = None
    port_to = None
    packet = None
    __plp = None
    __probability = 0.1	# Higher probability means Higher losses rate

    def __init__(self, ip_from, port_from, ip_to, port_to, packet):
        self.ip_from = ip_from
        self.port_from = port_from
        self.ip_to = ip_to
        self.port_to = port_to
        self.packet = packet
        #self.setprobability()
    def setprobability(self):
        """
		Simulate the Packet Loss with defining a random probability
		"""
        self.__plp = int(random.uniform(0, 1) + self.__probability)

    def isLost(self):
        """

		"""
        return self.__plp
