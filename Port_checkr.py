#!/usr/bin/env python3
#Coded By : A_Asaker

import socket
import sys,os,time
import threading
from urllib.request import urlopen
import ipaddress

socket.setdefaulttimeout(5)
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def usage():
	print('''	| Port Checker - By A_Asaker |
	~ Usage : ./Port_checkr.py [ host ] [ Port Number ]
		- host : 
			~ -l => local ip address, for this device.
			~ -p or -r => public/remote ip address, for this device.
			~ <ip address> => any other device ip address.
		- ports : ~ if port is under 1024, then you should run it 
			    with "sudo" [as a root].
	~ Example : ./Port_checkr.py -l 214
	~ Example : ./Port_checkr.py -r 214
	~ Example : ./Port_checkr.py 231.45.2.67 214''')
	sys.exit()

if len(sys.argv)<3:
	usage()
else:
	port=int(sys.argv[2])

try:
	myhost = urlopen('http://ip.42.pl/raw').read().decode('UTF-8')
	no_conn=0
except :
	no_conn=1

if sys.argv[1]=="-l":
	host=socket.gethostbyname(socket.gethostname())
	local=1
elif sys.argv[1]=="-r" or sys.argv[1]=="-p":
	if no_conn:
		print(" ~ There Is No Internet Access. ")
		sys.exit(0)
	host = myhost
	local=1
else:
	if no_conn:
		print(" ~ There Is No Internet Access. ")
		sys.exit(0)
	host=sys.argv[1]
	if(ipaddress.ip_address(host).is_private or host==myhost):
		local=1
	else:
		local=0

if port <1024 and local :
	if not os.geteuid() == 0:
		print(" ~ Ports Under 1024 Must Be Run As Root \"sudo\".")
		sys.exit(0)

established=0
srvr_est=0
exit_err=0
def serv_est():
	global established,srvr_est,exit_err
	try:
		server.bind(("0.0.0.0",port))
		server.listen(1)
		srvr_est=1
		conn,addr=server.accept()
		established=1
	except OSError as e:
		print(" [~] It Looks Like That There Are Some Other Applications Are Using Port '{}' !".format(port))
		exit_err=1
		sys.exit()
	except Exception as e:
		print(e)
		exit_err=1
		sys.exit()

def clnt_cnn():
	try:
		client.connect((host,port))
		if(sys.argv[1]=="-l"):
			print(" [#] Port {} [ Is Forwarded ] To This Device !".format(port))
		elif(sys.argv[1]=="-r" or sys.argv[1]=="-p"):
			time.sleep(.05)
			if (established):
				print(" [#] Port {} [ Is Forwarded ] On [{}] To This Device!".format(port,host))
			else:
				print(" [#] Port {} [ Is Forwarded ] On [{}] To Another Device!".format(port,host))
		else:
			if(local):
				print(" [#] Port {} [ Is Forwarded ] To This Device !".format(port))
			else:
				print(" [#] Port {} [ Is Opened ] On [{}] !".format(port,host))
	except ConnectionRefusedError as e:
		print(" [X] Port {} [ Is Not Forwarded/Opened ] On [{}] !".format(port,host))
		sys.exit()
	except Exception as e:
		print(" [X] Port {} [ Is Not Forwarded/Opened ] On [{}] !".format(port,host))
		sys.exit()

def main():
	if local:
		threading.Thread(target=serv_est,daemon=True).start()
		while not srvr_est and not exit_err:
			pass
	if exit_err:
		sys.exit(0)
	threading.Thread(target=clnt_cnn).start()

if __name__ == '__main__':
	main()
