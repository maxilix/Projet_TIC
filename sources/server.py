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
	print("Serveur stated, enter not empty line to exit\n")
	pid = os.fork()
	if not pid :
		run_server(s)
	else:
		while True:
			if (input() != ''):
				os.kill(pid,15)
				break




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
	print("Conected client : " + client[0])
	while True:
		otpServer = CreerOTP(client[1])
		otpClient = connexion.recv(32).decode('UTF-8')
		if(otpClient == otpServer):
			connexion.sendall("Authentification OK".encode('UTF-8'))
			break
		connexion.sendall("Please generate OTP with shared secret".encode('UTF-8'))
	clientChoice = connexion.recv(1024).decode('UTF-8')

	if(clientChoice == "generate_certificate"):
		# GENERATE CERTIFICATE
		certificateInfos = connexion.recv(1024).decode('UTF-8')[2:-2]
		certificateInfos = certificateInfos.split("', '")
		CreerAttestation.CreerAttestation(client, certificateInfos)
		connexion.sendall("certificate has been generated and sent to {}".format(certificateInfos[2]).encode('UTF-8'))

	else:
		# VERIFY CERTIFICATE
		while True:
			nbLinesToReceive = int(connexion.recv(128).decode('UTF-8'))
			print("\nNumber of lines to receive : " + str(nbLinesToReceive))

			certificateB64 = ""
			print("\t--> Waiting base64 image certificate")
			line = connexion.recv(1024).decode('UTF-8')
			while("finitiondutransfertdeimageB64" not in line):
				certificateB64 += line
				line = connexion.recv(1024).decode('UTF-8')
			print("\t--> Received base64 image certificate")

			print("\t--> Create base64 certificate file : ", end = '')
			fichier = open("../clients/{0}/sent_certificate.b64".format(client[0].replace(" ","-")),"w")
			fichier.write(certificateB64)
			fichier.close()
			print("OK")

			fichier = open("../clients/{0}/sent_certificate.b64".format(client[0].replace(" ","-")),"r")
			nbLinesReceived = len(fichier.readlines())
			print("\t--> Number of lines received : " + str(nbLinesReceived))
			fichier.close()
			if (nbLinesToReceive == nbLinesReceived):
				print("\t--> Reception completed")
				connexion.sendall("reception completed".encode('UTF-8'))
				break
			else:
				print("\t--> Reception failed")
				connexion.sendall("reception failed".encode('UTF-8'))

		print("\nCreate PNG certificate file : ", end = '')
		subprocess.run('''openssl base64 -base64 -d -in ../clients/{0}/sent_certificate.b64 -out ../clients/{0}/sent_certificate.png'''.format(client[0].replace(" ","-")), shell = True, stdout = subprocess.PIPE)
		print("OK")
		
		report = ExtrairePreuve.ExtrairePreuve(client,"sent_certificate.png")
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

