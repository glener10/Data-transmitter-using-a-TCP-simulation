#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'All'
__email__ = '{glenerpizzolato}, @gmail.com'
#__version__ = '{1}.{0}.{0}'

try:
	from socket import *
	import hashlib
	import random
	import argparse
	import datetime
	import string
except ImportError as error:
	print(error)
	print("1. Install requirements:")
	print("  pip install --upgrade pip")
	print("  pip install -r requirements.txt ")
	print()
	exit(-1)

DEFAULT_FRAME_SIZE = 1024					
DEFAULT_ERROR_PERCENTAGE = 0			
DEFAULT_PATH_INPUT = "./inputs/input.txt"

def random_generator(size=6, chars= string.ascii_uppercase + string.digits):	
	return ''.join(random.choice(chars) for _ in range(size))
class Transmitter:
	def __init__(self,serverName,serverPort,frame_size, error_percentage, input_file):
		self.serverName = serverName
		self.serverPort = serverPort
		self.destiny = (serverName, serverPort)
		self.tcp = socket(AF_INET,SOCK_DGRAM)
		self.error_percentage = error_percentage
		self.error_number = 0
		self.frame_size = frame_size

		self.number_of_packages = 0

		self.data = open(input_file,"r")
		self.data = self.data.read()
		self.data_size = len(self.data)

		self.read_number_of_packages()

	def read_number_of_packages(self):		
		for i in range(0,self.data_size-1,self.frame_size):
			self.number_of_packages += 1
	
	def check(self, transmission_check,aux):			
		if(transmission_check != " "):	
			if(transmission_check == "ACK"):
				print ("Sending: %s   Receptor: ACK" %aux)
			else:
				if(transmission_check == "NACK"):
					print ("Sending: %s   Receptor: NACK" %aux)
				else:
					print ("Sending: %s   Receptor: NACK" %aux)
		else:
			print ("Sending: %s   Receptor: NACK" %aux)	
	
	def send(self):								

		try:
			self.tcp.settimeout(None)
			self.tcp.sendto(("%s|%s"%(self.number_of_packages,self.frame_size)),self.destiny)		
		except ImportError as e:
			print("Error sending number of packets and frame size from file to be transmitted")

		for i in range(0,self.data_size-1,self.frame_size):

			error_auxiliary = ""
			transmission_check = ""

			h = hashlib.new('md5')
			aux = self.data[i:i+self.frame_size]
			h.update(aux)
		
			waiting_time = random.randrange(1, 101)

			if(waiting_time >= self.error_percentage):		
				self.tcp.sendto(aux,(self.destiny))			
				self.tcp.sendto(h.hexdigest(),(self.destiny))
				transmission_check, serverAddress = self.tcp.recvfrom(2048)	
				self.check(transmission_check,aux)
			else:
				while(waiting_time <= self.error_percentage):	
					self.error_number += 1						
					waiting_time = random.randrange(1, 101)
					error_auxiliary = random_generator(self.frame_size)
					self.tcp.sendto(error_auxiliary,(self.destiny))
					self.tcp.sendto(h.hexdigest(),(self.destiny))
					transmission_check, serverAddress = self.tcp.recvfrom(2048)
					self.check(transmission_check,aux)

				self.tcp.sendto(aux,(self.destiny))
				self.tcp.sendto(h.hexdigest(),(self.destiny))
				transmission_check, serverAddress = self.tcp.recvfrom(2048)
				self.check(transmission_check,aux)

	def close_socket(self):
		self.tcp.close()


def add_arguments(parser):
	parser.add_argument("--frame", "-f", help="frame size", default=DEFAULT_FRAME_SIZE, type=int)
	parser.add_argument("--erro", "-e", help="error percentage", default=DEFAULT_ERROR_PERCENTAGE, type=int)
	parser.add_argument("--input", "-i", help="input file", default=DEFAULT_PATH_INPUT, type=str)
	return parser

def main():
	parser = argparse.ArgumentParser(description='Transmitter Socket UDP')
	parser = add_arguments(parser)
	args = parser.parse_args()

	time_begin = datetime.datetime.now()

	try:
		transmitter = Transmitter("localhost",12000, args.frame, args.erro, DEFAULT_PATH_INPUT)
		transmitter.send()

	except ImportError as e:
		print("Error starting transmission")

	time_end = datetime.datetime.now()
	time_diff = (time_end - time_begin)
	time_diff_seconds = time_diff.seconds + (time_diff.microseconds/1000000.0)

	#print ("Final Message sent: %s"%complete_output)

	print ("Number of errors: %d"%transmitter.error_number)
	print ("Number of packages: %d"%transmitter.number_of_packages)
	print ("Total time transmition: {}\n".format(time_diff_seconds))

	transmitter.close_socket()

if __name__ == '__main__':
	exit(main())