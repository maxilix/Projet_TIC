#!/usr/bin/python3


import subprocess
import image_management


def CreerAtestation():

	# demande des information personel
	name = input("Nom du propriétaire : ")
	firstName = input("Prénom du propriétaire : ")
	mail = input("Adresse email du propriétaire : ")
	entitle = input("Intitulé de la certification : ")
	print()

	# demande du mot de passe OTP
	oneTimePassword = input("Mot de passe : ")

	# Vérification de l'OTP avec sortie erreur
	

	#
	# calcul du timestamp et construction de fichier (fonction create_timestamp)
	#


	# constrution du bloc d'information (Nom Prénom intituler certification) +timestamp
	personnal_data_filename = create_personal_data_file(name, firstName, mail, entitle)
	timestamp = create_timestamp(personnal_data_filename)

	#creation du qrcode
	image_management.create_qrcode_image(data,qrcodeFileName)

	# creation de l'image
	image_management.create_texte_image(firstName,name, texteFileName)


	# stégano de l'image

	# itégration du qrcode a l'image


	# envoie de l'image finie par email.



def create_personal_data_file(name, firstName, mail, entitle):

	subprocess.run('''rm personnal_data_{}{}'''.format(firstName[0],name), shell = True, stdout = subprocess.PIPE )
	fichier = open("personnal_data_{}{}".format(firstName[0],name),"w")

	fichier.write(name + '\n')
	fichier.write(firstName + '\n')	
	fichier.write(mail + '\n')
	fichier.write(entitle + '\n')

	fichier.close()

	return "personnal_data_{}{}".format(firstName[0],name) 

def create_timestamp(fichier): #fichier = personnal_data_FName
	fName = str(fichier).split('_')[2]

	#subprocess.run("rm query.tsq query.tsr", shell=True,stdout=subprocess.PIPE)

	commande = subprocess.Popen('''openssl ts -query -data {0} -sha1 -out query_{1}.tsq'''.format(fichier, fName) , shell=True,stdout=subprocess.PIPE)
	#query.tsq contient la requête, empreinte calculée avec sha1
	(resultat, ignorer) = commande.communicate()

	#Ensuite, on envoie la requête au serveur d'horodatage
	commande = subprocess.Popen('''curl -H "Content-Type: application/timestamp-query" --data-binary '@query_{0}.tsq' https://freetsa.org/tsr > timestamp_sign_{0}.tsr'''.format(fName) , shell=True,stdout=subprocess.PIPE)
	(resultat,ignorer) = commande.communicate()

	#Recupération timestamp
	commande = subprocess.Popen('''openssl ts -reply -in timestamp_sign_{}.tsr -text'''.format(fName),shell=True,stdout=subprocess.PIPE)
	(resultat,ignorer) = commande.communicate()
	resultat = str(resultat).split('Time stamp: ')
	timestamp = resultat[1].split('\\n')[0] #timestamp en string
	commande = subprocess.Popen('''date -d "{}" +%s'''.format(timestamp),shell=True,stdout=subprocess.PIPE)
	(resultat,ignorer) = commande.communicate()
	timestamp = str(resultat)[2:-3] #timestamp en seconde
	return timestamp



