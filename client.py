#!/usr/bin/python3

import socket
import sys
import base64
import subprocess
import time

from datetime import timedelta
from datetime import datetime



NUMERO_PORT = 8820



def CreerOTP(secret): # Google Authentificator code
	key = base64.b32decode(secret)
	date = str(subprocess.run('date +%s',shell=True,stdout=subprocess.PIPE))
	date = date[date.find('stdout') + 9:-4]
	m = int(date) // 30
	hashMac = str(subprocess.run('echo -n {} | openssl sha1 -hmac {}'.format(date, key), shell=True, stdout=subprocess.PIPE))
	hashMac = hashMac[hashMac.find('stdout') + 18 : -4]
	truncatedHashMac = hex(int(hashMac,16) & 0x7fffffff)
	otp = str(int(truncatedHashMac, 16) % 1000000).zfill(6)
	return otp



def start_client(clientName, passphrase, user):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect(('localhost', NUMERO_PORT))
	except Exception as e:
		print("Unable to connect")
		sys.exit(1)
	s.sendall(clientName.encode('UTF-8'))
	if(s.recv(1024).decode('UTF-8') == "Hi, plz send moni"):
		print('name not in server database')
		s.close()
		sys.exit(1)
	otpClient = CreerOTP(base64.b32encode(passphrase.encode('UTF-8')))
	s.sendall(otpClient.encode('UTF-8'))
	if(s.recv(1024).decode('UTF-8') == "Please generate OTP with shared secret"):
		otpClient = CreerOTP(base64.b32encode(passphrase.encode('UTF-8')))
		s.sendall(otpClient.encode('UTF-8'))
		if(s.recv(1024).decode('UTF-8') == "Please generate OTP with shared secret"):
			print('wrong passphrase')
			s.close()
			sys.exit(1)
	choice = 0
	print('CP')
	while(int(choice) != 1 and int(choice) != 2):
		choice = input('[1] generated certificate  or  [2] verify certificate  : ')
	if (int(choice) == 1):
		s.sendall("generate_certificate".encode('UTF-8'))
		s.sendall(str(user).encode('UTF-8'))
		print(s.recv(1024).decode('UTF-8'))
	else:
		s.sendall("verify_certificate".encode('UTF-8'))
		send_certificate(s)
		print(s.recv(1024).decode('UTF-8'))
	s.close()


def send_certificate(s):
	certificateFileName = input("Filename's certificate in curent path : ")
	cmd = subprocess.Popen('''openssl base64 -base64 -e -in {0} -out base64_{0}'''.format(certificateFileName), shell = True, stdout = subprocess.PIPE)
	cmd.communicate()
	fd = open("base64_"+certificateFileName)
	lines = fd.readlines()
	fd.close()
	print("send first line")
	for line in lines:
		s.sendall(line.encode('UTF-8'))
		pause()
	print("sent")
	s.sendall("finitiondutransfertdeimageB64".encode('UTF-8'))

def pause():
	debut = datetime.now()
	while (True):
		if (datetime.now()-debut > timedelta(seconds=0, milliseconds=0, microseconds=10)):
			break




#user = [ "Hoffmann" , "Clement"  , "clement.hoffmann@etu.unilim.fr" , "Plongée" ]
#user = [ "Beltzer"  , "Baptiste" , "baptiste.beltzer@etu.unilim.fr" , "Python"  ]
user = [ "Vollmer"  , "Morgane"  , "morgane.vollmer@etu.unilim.fr"  , "Sieste"  ]

start_client("CertifPlus", "LAME6SECRET",user)