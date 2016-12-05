import hashlib
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
