#!/usr/bin/env python3
# Coded By : A_Asaker

import socket
import sys
import threading
from urllib.request import urlopen

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def usage():
	print('''	| Port Forwarding Checker - By A_Asaker |
	~ Usage : ./Port_checkr.py [ Port Number ]
	~ Example : ./Port_checkr.py 214''')
	sys.exit()

if len(sys.argv)==1:
	usage()
else:
	port=int(sys.argv[1])

host = urlopen('http://ip.42.pl/raw').read().decode('UTF-8')

def serv_est():
	try:
		server.bind(("0.0.0.0",port))
		server.listen(1)
		conn,addr=server.accept()
	except OSError as e:
		print(" [#] There May Be Some Other Applications Are Using Port {} !".format(port))
		sys.exit()
	except Exception as e:
		print(e)
		sys.exit()

def clnt_cnn():
	try:
		client.connect((host,port))
		print(" [#] Port {} [ Is Forwarded ] For This Device!".format(port))
	except ConnectionRefusedError as e:
		print(" [#] Port {} [ Is Not Forwarded ] For This Device!".format(port))
		sys.exit()
	except Exception as e:
		print(" [#] Port {} [ Is Not Forwarded ] For This Device!".format(port))
		sys.exit()

def main():
	threading.Thread(target=serv_est,daemon=True).start()
	threading.Thread(target=clnt_cnn).start()

if __name__ == '__main__':
	main()
