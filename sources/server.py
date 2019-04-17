#!/usr/bin/python3

import subprocess, socket, os, sys, base64
import CreerAttestation
import ExtrairePreuve

PORT_NUMBER = 8820



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



def start_server():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(('', PORT_NUMBER))
	s.listen()
	run_server(s)



def run_server(s):
	clients = get_clients()
	while True:
		(connexion, TSAP) = s.accept()
		pid = os.fork()
		if not pid:
			break
	clientNameOk = False
	while not clientNameOk:
		clientName = connexion.recv(1024).decode('UTF-8')
		for customer in clients:
			if customer[0] == clientName:
				clientNameOk = True
				client = customer.copy()
				connexion.sendall("Please generate OTP with shared secret".encode('UTF-8'))
		if not clientNameOk:
			connexion.sendall("Hi, plz send money".encode('UTF-8'))
	print("conected client : " + client[0])
	while True:
		otpServer = CreerOTP(client[1])
		otpClient = connexion.recv(32).decode('UTF-8')
		if(otpClient == otpServer):
			connexion.sendall("Authentification OK".encode('UTF-8'))
			break
		connexion.sendall("Please generate OTP with shared secret".encode('UTF-8'))
	clientChoice = connexion.recv(1024).decode('UTF-8')
	if(clientChoice == "generate_certificate"):
		certificateInfos = connexion.recv(1024).decode('UTF-8')[2:-2]
		certificateInfos = certificateInfos.split("', '")
		CreerAttestation.CreerAttestation(client, certificateInfos)
		connexion.sendall("certificate has been generated and sent to {}".format(certificateInfos[2]).encode('UTF-8'))

	else:
		certificateB64 = ""
		print("wait first line")
		line = connexion.recv(1024).decode('UTF-8')
		while("finitiondutransfertdeimageB64" not in line):
			certificateB64 += line
			line = connexion.recv(1024).decode('UTF-8')
		report = ExtrairePreuve.ExtrairePreuve(client,certificateB64)
		connexion.sendall(report.encode('UTF-8'))




def get_clients():	# Return a list of clients' infos
	f = open('../clients/clients_database', 'r')
	fc = f.readlines()
	clients = []
	for client in fc:
		client = client[:-1]
		clients.append(client.split("\t"))
	f.close()
	return clients


start_server()

