import subprocess

def CreerAttestation():

	name = input("Nom du propriétaire : ")
	firstName = input("Prénom du propriétaire : ")
	mail = input("Adresse email du propriétaire : ")
	entitle = input("Intitulé de la certification : ")


 	subprocess.run('''rm personnal_data_{}{}'''.format(firstName[0],name), shell = False, stdout = subprocess.PIPE )
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
	commande = subprocess.Popen('''curl -H "Content-Type: application/timestamp-query" --data-binary '@query_{0}.tsq' https://freetsa.org/tsr > timestamp_sign_{0}'''.format(fName) , shell=True,stdout=subprocess.PIPE)
	(resultat,ignorer) = commande.communicate()

	#Recupération timestamp
	commande = subprocess.Popen('''openssl ts -reply -in timestamp_sign_{} -text'''.format(fName),shell=True,stdout=subprocess.PIPE)
	(resultat,ignorer) = commande.communicate()
	resultat = str(resultat).split('Time stamp: ')
	timestamp = resultat[1].split('\\n')[0] #timestamp en string
	commande = subprocess.Popen('''date -d "{}" +%s'''.format(timestamp),shell=True,stdout=subprocess.PIPE)
	(resultat,ignorer) = commande.communicate()
	timestamp = str(resultat)[2:-3] #timestamp en seconde
	return timestamp


CreerHorodatage(CreerAttestation())

