#!/usr/bin/python3


import subprocess
import os
import smtplib
import image_management
import data_management

def CreerAttestation(client,informations):
	pathClient = "../clients/"+client[0].replace(" ","-")+"/"
	if not (os.path.isdir(pathClient)):
		print("failded to access to the client repository")
		return

	path = pathClient+informations[0].replace(" ","-")+"_"+informations[1].replace(" ","-")+"_"+informations[3].replace(" ","-")+"/"
	#print(path)

	if not (os.path.isdir(path)):
		print("generating certificate ...")
		print('''mkdir {}'''.format(path[:-1]))
		subprocess.run('''mkdir {}'''.format(path[:-1]), shell = True, stdout = subprocess.PIPE)
		create_mail_file(path,informations[2])
		create_personal_data_file(path, informations[0], informations[1], informations[3])
		create_query_file(path)
		create_timestamp_file(path)
		create_user_auth_data(informations,path)

		biBlock = data_management.create_block(path, informations[0], informations[1], informations[3])
		qrcodeData = "tata"
		image_management.create_assembled_stegano_image(path, informations[0], informations[1], informations[3], biBlock, qrcodeData)

		print("\t--> generated certificate !")
	else:
		print("certificate has been already generated")
	print("sending mail ...")
	subprocess.run('''echo "Content-Type: image/png\r\nContent-Transfer-Encoding: base64\r\n" > {0}contenu.txt'''.format(path), shell=True,stdout=subprocess.PIPE)
	subprocess.run('''openssl base64 -base64 -e -in {0}certificate.png >> {0}contenu.txt'''.format(path), shell=True,stdout=subprocess.PIPE)
	subprocess.run('''echo "basicConstraints=critical,CA:FALSE\r\nextendedKeyUsage=serverAuth,emailProtection\r\nkeyUsage=digitalSignature,keyEncipherment" > {0}cert.cnf'''.format(path), shell=True,stdout=subprocess.PIPE)
	subprocess.run('''openssl x509 -req -days 3650 -CA {0}ca.cert.pem -CAkey {0}ca.key -CAcreateserial -extfile {1}cert.cnf -in {1}csr.pem -out {1}certifmail.pem'''.format(pathClient,path), shell=True,stdout=subprocess.PIPE)
	
	subprocess.run('''openssl cms -sign -in {0}contenu.txt -signer {0}certifmail.pem -inkey {0}key.pem -text | openssl cms -encrypt -out {0}mail.msg -from {1} -to {2} -subject "Votre certificat" -aes256 {0}certifmail.pem'''.format(path,client[2],informations[2]), shell=True,stdout=subprocess.PIPE)
	f = open(path + "mail.msg",'r')
	lines = f.readlines()
	f.close()
	secureMail = ""
	for line in lines:
		secureMail += line
	s = smtplib.SMTP_SSL("smtp.unilim.fr",465)
	#s.set_debuglevel(1)
	#s.login('beltzer01', '1aAzerty')
	s.sendmail(client[2],informations[2],secureMail)
	s.close()
	print("\t--> sent mail !")



def create_user_auth_data(informations, path):
	subprocess.run('''openssl ecparam -out {0}key.pem -name prime256v1 -genkey'''.format(path), shell=True,stdout=subprocess.PIPE)
	subprocess.run('''echo "[req]\r\ndistinguished_name=dn\r\n[dn]\r\n[ext]\r\nbasicConstraints=CA:FALSE\r\nextendedKeyUsage=serverAuth,emailProtection\r\nkeyUsage=digitalSignature,keyEncipherment" > {0}csr.cnf'''.format(path), shell=True,stdout=subprocess.PIPE)
	subprocess.run('''openssl req -config {0}csr.cnf -new -subj "/CN={1} {2}/emailAddress={3}" -reqexts ext -sha256 -key {0}key.pem -out {0}csr.pem'''.format(path, informations[1], informations[0], informations[2]), shell=True,stdout=subprocess.PIPE)


def create_mail_file(path,mail):
	fichier = open("{}mail_address".format(path),"w")
	fichier.write(mail + '\n')
	fichier.close()


def create_personal_data_file(path, name, firstName, entitle):
	fichier = open("{}personnal_data".format(path),"w")
	fichier.write(name + '\n')
	fichier.write(firstName + '\n')	
	fichier.write(entitle + '\n')
	fichier.close()


def create_query_file(path):
	cmd = subprocess.Popen('''openssl ts -query -data {0}personnal_data -sha1 -no_nonce -out {0}query.tsq'''.format(path) , shell=True,stdout=subprocess.PIPE)
	#query.tsq contient la requête, empreinte calculée avec sha1
	cmd.communicate()


def create_timestamp_file(path):#fichier): #fichier = personnal_data_FName
	#On envoie la requête au serveur d'horodatage
	cmd = subprocess.Popen('''curl -H "Content-Type: application/timestamp-query" --data-binary '@{0}query.tsq' https://freetsa.org/tsr > {0}timestamp_sign.tsr'''.format(path) , shell=True,stdout=subprocess.PIPE)
	cmd.communicate()
	
	#Recupération timestamp
	#cmd = subprocess.Popen('''openssl ts -reply -in {0}timestamp_sign.tsr -text'''.format(path),shell=True,stdout=subprocess.PIPE)
	#(result,ignore) = cmd.communicate()
	#result = str(result).split('Time stamp: ')
	#timestamp = result[1].split('\\n')[0] #timestamp en string
	#cmd = subprocess.Popen('''date -d "{}" +%s'''.format(timestamp),shell=True,stdout=subprocess.PIPE)
	#(result,ignore) = cmd.communicate()
	#timestamp = str(result)[2:-3] #timestamp en seconde
	#return timestamp


#c = [ "CertifPlus" , "LAME6SECRET" , "ecc.certifplus.ca.pem" , "comunication@certifplus.fr" ]
#i = [ "Beltzer" , "Baptiste" , "baptiste.beltzer@etu.unilim.fr" , "Python" ]


#CreerAttestation(c,i)