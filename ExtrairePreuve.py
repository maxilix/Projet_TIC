import subprocess
import os
import image_management
import data_management
from PIL import Image





def ExtrairePreuve():
	name = input("Nom du propriétaire : ")
	firstName = input("Prénom du propriétaire : ")
	path = "./{}_{}/".format(name.replace(" ","-"),firstName.replace(" ","-"))
	if not (os.path.isdir(path[:-1])):
		print("Aucun utilisateur au non de {}".format(path[2:-1]))
		return
	if not (os.path.exists("{}certificate.png".format(path))):
		print("Pas encore de certification au nom de {}".format(path[2:-1]))
		return

	certificateImage = Image.open("{}certificate.png".format(path))
	block = image_management.recuperer(certificateImage,2654)
	(blockNameReturned, blockFirstNameReturned, blockEntitleReturned, blockTimestampAsciiReturned) = data_management.cut_block(block)

	if ((name != blockNameReturned) or (firstName != blockFirstNameReturned)):
		print("Erreur, informations nominatives falcifiées !")
	chekingTimestampFile = open("{}checking_timestamp_sign.tsr".format(path),'wb')
	blockTimestampAsciiReturnedList = [blockTimestampAsciiReturned[2*i]+blockTimestampAsciiReturned[2*i+1] for i in range(len(blockTimestampAsciiReturned)//2)]
	#print(blockTimestampAsciiReturnedList)
	for octet in blockTimestampAsciiReturnedList:
		#print(octet)
		chekingTimestampFile.write(int(octet,16).to_bytes(1,byteorder='big',signed=False))
	chekingTimestampFile.close()

	cmd = subprocess.Popen('''openssl ts -verify -in {0}checking_timestamp_sign.tsr -queryfile {0}query.tsq -CAfile cacert.pem -untrusted tsa.crt'''.format(path), shell=True, stdout=subprocess.PIPE)
	(result,ignore) = cmd.communicate()
	subprocess.rum('''rm {}}checking_timestamp_sign.tsr'''.format(path))
	if not('OK' in str(result)):
		print("Erreur, timestamp altéré")


	# VERIFICATION QRCODE

	print("Vérification complétée : Le certificat de {0} {1} est autentique".format(firstName,name))







ExtrairePreuve()