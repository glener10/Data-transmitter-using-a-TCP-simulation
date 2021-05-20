# (C) 2020 Glener Lanes Pizzolato

from socket import *
import hashlib
import os
import time
import random
import argparse
import datetime
import numpy as np
import string

class Receptor:
    def __init__(self,serverPort):
        self.serverPort = serverPort
        self.tcp = socket(AF_INET, SOCK_DGRAM)
        self.tcp.bind(('', self.serverPort))

        self.output_data = ""       #Tudo que o servidor recebeu

        self.number_of_packages = 0 #Numero total de pacotes
        self.extension = ""         #Extensao do arquivo (.mp3,.ppm,.jpg,.txt,etc)


    def __read_number_packages(self):
        self.number_of_packages = self.tcp.recvfrom(2048)
        self.number_of_packages = int(self.number_of_packages[0])
    
    def __read_extension(self):
        self.extension = self.tcp.recvfrom(2048)
        self.extension = str(self.extension[0])

    def transmission(self):
        self.__read_number_packages()
        self.__read_extension()

        i = 0
        while (i < self.number_of_packages):
            h = hashlib.new('md5')
            frame, clientAddress = self.tcp.recvfrom(2048)
            hash, clientAddress = self.tcp.recvfrom(2048)

            h.update(frame)
            check_hash = h.hexdigest()
            if(hash == check_hash):
                self.output_data += frame
                print ("Receives: {}  Hash: {}  Block: {}".format(frame,hash,i))	
                self.tcp.sendto("ACK",clientAddress)
                i = i + 1
            else:
                print ("Error block: {}".format(i))					
                self.tcp.sendto("NACK",clientAddress)

def main():

    Socket = Receptor(12000)
    Socket.transmission()

    output = open(("Output.%s"%Socket.extension),"w")
    output.write(Socket.output_data)
main()
