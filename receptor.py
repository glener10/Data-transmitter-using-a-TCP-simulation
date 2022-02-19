#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'All'
__email__ = '{glenerpizzolato}, @gmail.com'
#__version__ = '{1}.{0}.{0}'

try:
    from socket import *
    import hashlib
    import argparse

except ImportError as error:
	print(error)
	print("1. Install requirements:")
	print("  pip install --upgrade pip")
	print("  pip install -r requirements.txt ")
	print()
	exit(-1)

DEFAULT_PORT = 12000
class Receptor:
    def __init__(self,serverPort):
        self.serverPort = serverPort
        self.tcp = socket(AF_INET, SOCK_DGRAM)
        self.tcp.bind(('', self.serverPort))
        self.output_data = ""      

    def read_information(self):
        information = self.tcp.recvfrom(2048)[0]
        self.number_of_packages = int(information.split('|')[0])
        self.frame_size = int(information.split('|')[1])
    
    def transmission(self):
        try:
            self.read_information()
        except ImportError as e:
            print("Error reading number of packets and frame size from file to be transmitted")

        i = 0
        while (i < self.number_of_packages):
            h = hashlib.new('md5')
            frame, clientAddress = self.tcp.recvfrom(self.frame_size)
            hash, clientAddress = self.tcp.recvfrom(self.frame_size)

            h.update(frame)
            check_hash = h.hexdigest()
            if(hash == check_hash):
                self.output_data += frame
                #print ("Receives: {}  Hash: {}  Block: {}".format(frame,hash,i))	
                print ("Block: {} - Hash: {}".format(i+1,hash))	
                self.tcp.sendto("ACK",clientAddress)
                i = i + 1
            else:
                print ("Error block: {}".format(i+1))					
                self.tcp.sendto("NACK",clientAddress)

def add_arguments(parser):
    parser.add_argument("--port", "-p", help="port", default=DEFAULT_PORT, type=int)
    return parser

def main():
    parser = argparse.ArgumentParser(description='Receptor Socket UDP')
    parser = add_arguments(parser)
    args = parser.parse_args()

    try:
        receptor = Receptor(args.port)
        receptor.transmission()
        output = open(("Output"),"w")
        output.write(receptor.output_data)
    except ImportError as e:
        print("Error while transmitting")


if __name__ == '__main__':
    exit(main())