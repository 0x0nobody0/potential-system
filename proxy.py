#!/bin/python3

import socket
from threading import Thread
import sys
from colorama import Fore, Back, Style
import parser
from importlib import reload


class Proxy2Server(Thread):
	def __init__(self, host, port):
		super(Proxy2Server, self).__init__()
		self.client = None # client will be set later in proxy
		self.port = port # server port
		self.host = host # server IP
		#creating socket connection
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.connect((host, port))
		# connection established

	def run(self):
		while True:
			data = self.server.recv(4096) # recieving data from server
			if data:
				try:
					reload(parser)
					parser.parse(data, self.port, 'server')
					data = parser.modify(data)
				except Exception as e:
					print ("server[{}]".format(self.port), e)

				#print("{}({},{}) ->{}".format(Fore.BLUE, self.host, self.port, data.decode("utf-8"), Fore.WHITE))
				self.client.sendall(data) # sending data to client


class Client2Proxy(Thread):
	def __init__(self, host, port):
		super(Client2Proxy, self).__init__()
		self.server = None # server will be allocated later in proxy
		self.port = port # client port
		self.host = host # client IP
		# creating socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind((host, port))
		sock.listen(1)
		self.client, address = sock.accept()
		# connection established

	def run(self):
		while True:
			data = self.client.recv(4096) # recieving data from client
			if data:
				try:
					reload(parser)
					parser.parse(data, self.port, 'client')
					data = parser.modify(data)
				except Exception as e:
					print ("client[{}]".format(self.port), e)
				#print("{}({},{}) ->{}".format(Fore.BLUE, self.host, self.port, data.decode("utf-8"), Fore.WHITE))
				self.server.sendall(data) # sending data to server

class Proxy(Thread):
	def __init__(self, from_host, from_port, to_host, to_port):
		super(Proxy, self).__init__()
		self.from_host = from_host # client ip
		self.to_host = to_host # server ip
		self.from_port = from_port # client port
		self.to_port = to_port #server port

	def run(self):
			print("[proxy({})] setting up".format(from_port))
			self.c2p = Client2Proxy(self.from_host, self.from_port) 
			self.p2s = Proxy2Server(self.to_host, self.to_port)
			self.c2p.server = self.p2s.server
			self.p2s.client = self.c2p.client
			self.c2p.start()
			print("[client({},{})] Connection established".format(from_host,from_port))
			self.p2s.start()
			print("[server({},{})] Connection established".format(to_host,to_port))


args = len(sys.argv)-1
if(args == 4):
	from_host = sys.argv[1]
	from_port = int(sys.argv[2])
	to_host = sys.argv[3]
	to_port = int(sys.argv[4])
	proxy_server = Proxy(from_host, from_port, to_host, to_port)
	proxy_server.start()
else:
	print("{}usage: {}from_host from_port to_host to_port".format(Fore.RED,Fore.YELLOW))
