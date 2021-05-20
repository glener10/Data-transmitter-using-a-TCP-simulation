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

DEFAULT_FRAME_SIZE = 4						
DEFAULT_ERROR_PERCENTAGE = 2			#2% a cada pacote de acontecer erro

DEFAULT_PATH_INPUT = "./inputs/"
DEFAULT_INPUT_FILE = "input.txt"

def random_generator(size=6, chars= string.ascii_uppercase + string.digits):	#Gera String aleatorio com tamanho arbitrario
	return ''.join(random.choice(chars) for _ in range(size))

class Transmitter:
	def __init__(self,serverName,serverPort,frame_size, error_percentage, input_file, extension_data):
		self.serverName = serverName
		self.serverPort = serverPort
		self.destiny = (serverName, serverPort)
		self.tcp = socket(AF_INET,SOCK_DGRAM)
		self.error_percentage = error_percentage
		self.error_number = 0
		self.frame_size = frame_size

		self.extension_data = extension_data

		self.data = open(input_file,"r")
		self.data = self.data.read()
		self.tam_data = len(self.data)

		self.number_of_packages=0
		self.__read_number_of_packages()


	def __read_number_of_packages(self):		#Define o numero de pacotes de acordo com o tamanho da entrada
		for i in range(0,self.tam_data-1,self.frame_size):
			self.number_of_packages += 1
	
	def verifica(self, confere,aux):			#Funcao print para informar a situacao de um dado pacote
		if(confere != " "):	
			if(confere == "ACK"):
				print ("Sending: %s   Receptor: ACK" %aux)
			else:
				if(confere == "NACK"):
					print ("Sending: %s   Receptor: NACK" %aux)
				else:
					print ("Sending: %s   Receptor: NACK" %aux)
		else:
			print ("Sending: %s   Receptor: NACK" %aux)	

	
	def send(self):								#Realiza a transmissao

		self.tcp.settimeout(None)

		self.tcp.sendto(("%s"%self.number_of_packages),self.destiny)	#Envia o numero de pacotes total para o receptor
		self.tcp.sendto(("%s"%self.extension_data),self.destiny)	#Envia a extensao do arquivo input

		for i in range(0,self.tam_data-1,self.frame_size):

			aux_erro = ""
			confere = ""

			h = hashlib.new('md5')
			aux = self.data[i:i+self.frame_size]
			h.update(aux)
		
			tempo_espera = random.randrange(1, 101)

			if(tempo_espera >= self.error_percentage):		#NAO ACONTECE ERRO, ENVIA HASH E MENSAGEM DE FORMA CORRETE
				self.tcp.sendto(aux,(self.destiny))			#ENVIA MENSAGEM
				self.tcp.sendto(h.hexdigest(),(self.destiny))	#ENVIA HASH
				confere, serverAddress = self.tcp.recvfrom(2048)	#RECEBE CONFIRMACAO DO SERVIDOR
				self.verifica(confere,aux)
			else:
				while(tempo_espera <= self.error_percentage):	#ACONTECE ERRO, ENVIA HASH E UMA MENSAGEM MODIFICADA (HOUVE ALTERACAO NA MENSAGEM DURANTE A TRANSMISSAO)
					self.error_number += 1						#OUTRA FORMA DE GERAR ERRO SERIA DEFINIR UM ATRASO NO RECEPTOR (IDEIA DE IMPLEMENTACAO FUTURA)
					tempo_espera = random.randrange(1, 101)
					aux_erro = random_generator(self.frame_size)
					self.tcp.sendto(aux_erro,(self.destiny))
					self.tcp.sendto(h.hexdigest(),(self.destiny))
					confere, serverAddress = self.tcp.recvfrom(2048)
					self.verifica(confere,aux)

				self.tcp.sendto(aux,(self.destiny))
				self.tcp.sendto(h.hexdigest(),(self.destiny))
				confere, serverAddress = self.tcp.recvfrom(2048)
				self.verifica(confere,aux)

	def close_socket(self):
		self.tcp.close()


# log = open("log.txt","w")
def main():
	parser = argparse.ArgumentParser(description='Socket UDP')
	parser.add_argument("--frame", "-f", help="frame size", default=DEFAULT_FRAME_SIZE, type=int)
	parser.add_argument("--erro", "-e", help="error percentage", default=DEFAULT_ERROR_PERCENTAGE, type=int)
	parser.add_argument("--input", "-i", help="input file", default=DEFAULT_INPUT_FILE, type=str)
	args = parser.parse_args()

	time_begin = datetime.datetime.now()

	Socket = Transmitter("localhost",12000, args.frame, args.erro, DEFAULT_PATH_INPUT + args.input, args.input.split(".")[1])
	Socket.send()

	time_end = datetime.datetime.now()
	time_diff = (time_end - time_begin)
	time_diff_seconds = time_diff.seconds + (time_diff.microseconds/1000000.0)

	#print ("Final Message sent: %s"%complete_output)

	print ("Number of errors: %d"%Socket.error_number)
	print ("Number of packages: %d"%Socket.number_of_packages)
	print ("Total time transmition: {}\n".format(time_diff_seconds))

	Socket.close_socket()

main()
