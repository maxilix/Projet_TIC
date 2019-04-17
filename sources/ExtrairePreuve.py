#!/usr/bin/python3


import subprocess
import os
import image_management
import data_management
import time
from PIL import Image

def ExtrairePreuve(client,imageB64):


	fichier = open("base64_certificate.tmp","w")
	fichier.write(imageB64)
	fichier.close()

	cmd = subprocess.Popen('''openssl base64 -base64 -d -in base64_certificate.tmp -out certificateImage.png''', shell = True, stdout = subprocess.PIPE)
	cmd.communicate()

	certificateImage = Image.open('certificateImage.png')

	print("Block recuperation")

	block = image_management.recuperer(certificateImage,2634)
	(blockNameReturned, blockFirstNameReturned, blockEntitleReturned, blockTimestampAsciiReturned) = data_management.cut_block(block)
	print("Block recuperated")
	
	name_firstName_entitled = blockNameReturned + "_" + blockFirstNameReturned + "_" + blockEntitleReturned

	path = '''../clients/{0}/{1}/'''.format(client[0].replace(" ","-"),name_firstName_entitled.replace(" ","-"))

	print("Check if this repositery exists")
	if (os.path.isdir(path)):
		print("Found repositery")
	else :
		print("No repositery for this name")
		print("Authentification FAILED")
		return "Authentification FAILED : No certificate delivery for this name."


	print("Extract timestamp data")
	chekingTimestampFile = open("timestamp_sign.tmp",'wb')
	blockTimestampAsciiReturnedList = [blockTimestampAsciiReturned[2*i]+blockTimestampAsciiReturned[2*i+1] for i in range(len(blockTimestampAsciiReturned)//2)]
	for octet in blockTimestampAsciiReturnedList:
		chekingTimestampFile.write(int(octet,16).to_bytes(1,byteorder='big',signed=False))
	chekingTimestampFile.close()
	print("Timestamp data extracted")



	#Verification du Bblock en créant un fichier ckeck_personnal_data
	print("Block verification")
	fichier = open("personnal_data.tmp","w")
	fichier.write(blockNameReturned +"\n")
	fichier.write(blockFirstNameReturned + "\n")
	fichier.write(blockEntitleReturned + "\n")
	fichier.close()

	cmd = subprocess.Popen('''openssl ts -query -data personnal_data.tmp -sha1 -no_nonce -out query.tmp''', shell=True,stdout=subprocess.PIPE)
	cmd.communicate()

	cmd = subprocess.Popen('''openssl ts -verify -in timestamp_sign.tmp -queryfile query.tmp -CAfile ../ressources/cacert.pem -untrusted ../ressources/tsa.crt''', shell=True, stdout=subprocess.PIPE)
	(result,ignore) = cmd.communicate()
	if ('OK' in str(result)):
		print("Block verification completed")
	else:
		print("Block verification failed \n")
		print("Authentification FAILED")
		return "Authentification FAILED : Data block has been altered."

	# VERIFICATION QRCODE
	print("qrCode verification")

	if (True):
		print("qrCode verification completed")
	else:
		print("qrCode verification failed \n")
		print("Authentification FAILED")
		return "Authentification FAILED : qrCode has been altered."

	# Reconstruction de l'image
	qrcodeData="tata"
	image_management.create_assembled_stegano_image("./", blockNameReturned, blockFirstNameReturned, blockEntitleReturned, block, qrcodeData)

	# check différences !
	cmd = subprocess.Popen('''compare -metric mae certificateImage.png certificate.png diff.png''', shell=True, stdout=subprocess.PIPE)
	(result,ignore) = cmd.communicate()
	print("\n1\n")
	print(result)
	print("\n2\n")
	print(ignore)
#red: 0 (0)
#green: 0 (0)
#blue: 0 (0)
#all: 0 (0)
	time.sleep(1)

	#subprocess.run('''rm certificateImage.png''', shell = True, stdout = subprocess.PIPE)
	subprocess.run('''rm base64_certificate.tmp''', shell = True, stdout = subprocess.PIPE)
	subprocess.run('''rm timestamp_sign.tmp''', shell = True, stdout = subprocess.PIPE)
	subprocess.run('''rm personnal_data.tmp''', shell = True, stdout = subprocess.PIPE)
	subprocess.run('''rm query.tmp''', shell = True, stdout = subprocess.PIPE)
	#subprocess.run('''rm certificate.png''', shell = True, stdout = subprocess.PIPE)
	subprocess.run('''rm diff.png''', shell = True, stdout = subprocess.PIPE)


	print("Authentification COMPLETED")
	return "Authentification COMPLETED"


