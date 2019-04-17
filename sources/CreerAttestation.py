#!/usr/bin/python3


import subprocess
import os
import image_management
import data_management

def CreerAttestation(client,informations):
	path = "../clients/"+client[0].replace(" ","-")
	if not (os.path.isdir(path)):
		print("failded to access to the client repository")
		return

	path = path+"/"+informations[0].replace(" ","-")+"_"+informations[1].replace(" ","-")+"_"+informations[3].replace(" ","-")+"/"
	#print(path)

	if not (os.path.isdir(path)):
		print("generating certificate ...")
		print('''mkdir {}'''.format(path[:-1]))
		subprocess.run('''mkdir {}'''.format(path[:-1]), shell = True, stdout = subprocess.PIPE)
		create_mail_file(path,informations[2])
		create_personal_data_file(path, informations[0], informations[1], informations[3])
		create_query_file(path)
		create_timestamp_file(path)

		biBlock = data_management.create_block(path, informations[0], informations[1], informations[3])
		qrcodeData = "tata"
		image_management.create_assembled_stegano_image(path, informations[0], informations[1], informations[3], biBlock, qrcodeData)

		print("generated certificate ...")
	else:
		print("certificate has been already generated")
	print("sending mail")
	# send mail
	print("sent mail")


def create_mail_file(path,mail):
	fichier = open("{}mail".format(path),"w")
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