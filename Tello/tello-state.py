#!/usr/bin/python

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1', 8889)
sock.bind(('',9000))

while True:
	try:
		data, server = sock.recvfrom(1024)
		print(data.decode())
	except Exception as err:
		print(err)
		sock.close()
		break
		
