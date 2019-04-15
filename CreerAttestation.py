#!/usr/bin/python3


import subprocess
import os
import image_management
import data_management


def CreerAtestation():

	# demande des information personel
	name = input("Nom du propriétaire : ")
	firstName = input("Prénom du propriétaire : ")
	path = "./{}_{}/".format(name.replace(" ","-"),firstName.replace(" ","-"))
	if not (os.path.isdir(path[:-1])):
		print("le dossier n'est pas prèt a l'emploit (OTP non généré)")
		return
	else:
		if (os.path.exists("{}personnal_data".format(path))):
			print("certification déja existante")
			return



	mail = input("Adresse email du propriétaire : ")
	entitle = input("Intitulé de la certification : ")
	print()

	# demande du mot de passe OTP
	oneTimePassword = input("Mot de passe : ")

	# Vérification de l'OTP avec sortie erreur
	otpFile = open("{}otp".format(path),'r')
	otpFile.readline()
	otp = otpFile.readline()[:-1]
	otpFile.close()
	if (oneTimePassword!=otp):
		print("He mec, tu t'es planté de mot de passe !")
		return
	print("Authentification réussi !")


	#
	# calcul du timestamp et construction de fichier (fonction create_timestamp)
	#


	# constrution du bloc d'information (Nom Prénom intituler certification) +timestamp
	create_personal_data_file(name, firstName, mail, entitle)
	timestamp = create_timestamp(name, firstName)

	# creation de l'image
	block = data_management.create_block(name,firstName,entitle)
	qrcodeData = "tata"
	image_management.create_assembled_stegano_image(firstName, name, entitle, block, qrcodeData)


	# stégano de l'image

	# itégration du qrcode a l'image


	# envoie de l'image finie par email.



def create_personal_data_file(name, firstName, mail, entitle):

	path = "./{}_{}/".format(name.replace(" ","-"),firstName.replace(" ","-"))

	fichier = open("{}personnal_data".format(path),"w")

	fichier.write(name + '\n')
	fichier.write(firstName + '\n')	
	fichier.write(mail + '\n')
	fichier.write(entitle + '\n')

	fichier.close()




def create_timestamp(name, firstName):#fichier): #fichier = personnal_data_FName
	#fName = str(fichier).split('_')[2]
	path = "./{}_{}/".format(name.replace(" ","-"),firstName.replace(" ","-"))
	#subprocess.run("rm query.tsq query.tsr", shell=True,stdout=subprocess.PIPE)

	cmd = subprocess.Popen('''openssl ts -query -data {0}personnal_data -sha1 -out {0}query.tsq'''.format(path) , shell=True,stdout=subprocess.PIPE)
	#query.tsq contient la requête, empreinte calculée avec sha1
	cmd.communicate()

	#Ensuite, on envoie la requête au serveur d'horodatage
	cmd = subprocess.Popen('''curl -H "Content-Type: application/timestamp-query" --data-binary '@{0}query.tsq' https://freetsa.org/tsr > {0}timestamp_sign.tsr'''.format(path) , shell=True,stdout=subprocess.PIPE)
	cmd.communicate()

	#Recupération timestamp
	cmd = subprocess.Popen('''openssl ts -reply -in {0}timestamp_sign.tsr -text'''.format(path),shell=True,stdout=subprocess.PIPE)
	(result,ignore) = cmd.communicate()
	result = str(result).split('Time stamp: ')
	timestamp = result[1].split('\\n')[0] #timestamp en string
	cmd = subprocess.Popen('''date -d "{}" +%s'''.format(timestamp),shell=True,stdout=subprocess.PIPE)
	(result,ignore) = cmd.communicate()
	timestamp = str(result)[2:-3] #timestamp en seconde
	return timestamp





CreerAtestation()