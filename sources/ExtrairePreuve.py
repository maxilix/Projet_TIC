#!/usr/bin/python3


import subprocess
import os
import image_management
import data_management
import time
from PIL import Image

def ExtrairePreuve(client,certificateFileNime):

	path = '''../clients/{}/'''.format(client[0].replace(" ","-"))
	certificateImage = Image.open(path+certificateFileNime)


	print("\nCheck image size")
	if (certificateImage.size == (1753,1240)):
		print("\t--> Right size : x=1753 and y=1240")
	else :
		print("\t--> Wrong size")
		print("\nAuthentification FAILED")
		remove_temp_file(path)
		return "Authentification FAILED : Wrong image size."


	print("\nExtract block data from steganography : ", end = '')
	block = image_management.recuperer(certificateImage,2634)
	(blockNameReturned, blockFirstNameReturned, blockEntitleReturned, blockTimestampAsciiReturned) = data_management.cut_block(block)
	print("OK")
	
	
	print("\nCheck if repositery exists")
	if (os.path.isdir(path+"{0}_{1}_{2}/".format(blockNameReturned.replace(" ","-"),blockFirstNameReturned.replace(" ","-"),blockEntitleReturned.replace(" ","-")))):
		print("\t--> Found repositery")
	else :
		print("\t--> No repositery for this name")
		print("\nAuthentification FAILED")
		remove_temp_file(path)
		return "Authentification FAILED : No certificate delivery for this name."


	print("\nExtract timestamp data from block : ", end='')
	chekingTimestampFile = open(path + "timestamp_sign.tmp",'wb')
	blockTimestampAsciiReturnedList = [blockTimestampAsciiReturned[2*i]+blockTimestampAsciiReturned[2*i+1] for i in range(len(blockTimestampAsciiReturned)//2)]
	for octet in blockTimestampAsciiReturnedList:
		chekingTimestampFile.write(int(octet,16).to_bytes(1,byteorder='big',signed=False))
	chekingTimestampFile.close()
	print("OK")


	print("\nBlock verification :")
	print("\t--> Create personnal_data file")
	fichier = open(path + "personnal_data.tmp","w")
	fichier.write(blockNameReturned +"\n")
	fichier.write(blockFirstNameReturned + "\n")
	fichier.write(blockEntitleReturned + "\n")
	fichier.close()
	print("\t--> Create query file")
	cmd = subprocess.Popen('''openssl ts -query -data {0}personnal_data.tmp -sha1 -no_nonce -out {0}query.tmp'''.format(path), shell=True,stdout=subprocess.PIPE)
	cmd.communicate()
	print("\t--> Verify TSA sing")
	cmd = subprocess.Popen('''openssl ts -verify -in {0}timestamp_sign.tmp -queryfile {0}query.tmp -CAfile ../ressources/cacert.pem -untrusted ../ressources/tsa.crt'''.format(path), shell=True, stdout=subprocess.PIPE)
	(result,ignore) = cmd.communicate()
	if ('OK' in str(result)):
		print("\t--> Block verification completed")
	else:
		print("\t--> Block verification failed")
		print("\nAuthentification FAILED")
		remove_temp_file(path)
		return "Authentification FAILED : Data block has been altered."


	print("\nQrCode verification :")
	if (True):
		print("\t--> QrCode verification completed")
	else:
		print("\t--> QrCode verification failed")
		print("\nAuthentification FAILED")
		remove_temp_file(path)
		return "Authentification FAILED : QrCode has been altered."


	print("\nRecreate image certificate :")
	print("\t--> Create QrCode sign")
	qrcodeData="tata"
	print("\t--> Create assembled stego cetificate")
	image_management.create_assembled_stegano_image(path, blockNameReturned, blockFirstNameReturned, blockEntitleReturned, block, qrcodeData)
	print("\t--> Recreate image certificate completed")


	print("\nCheck differences between sent and recreated certificate :")
	if image_management.check_identity_images(path,certificateFileNime,"certificate.png"):
		print("\t--> Check differences completed")
	else:
		print("\t--> Check differences failed")
		print("\nAuthentification FAILED")
		remove_temp_file(path)
		return "Authentification FAILED : Image certificate has been altered."


	print("\nAuthentification COMPLETED")
	remove_temp_file(path)
	return "Authentification COMPLETED"


def remove_temp_file(path):
	if os.path.isfile("{}certificate.png".format(path)):
		subprocess.run('''rm {}certificate.png'''.format(path)     , shell = True, stdout = subprocess.PIPE)
	
	if os.path.isfile("{}sent_certificate.png".format(path)):
		subprocess.run('''rm {}sent_certificate.png'''.format(path), shell = True, stdout = subprocess.PIPE)
	
	if os.path.isfile("{}sent_certificate.b64".format(path)):
		subprocess.run('''rm {}sent_certificate.b64'''.format(path), shell = True, stdout = subprocess.PIPE)
	
	if os.path.isfile("{}timestamp_sign.tmp".format(path)):
		subprocess.run('''rm {}timestamp_sign.tmp'''.format(path)  , shell = True, stdout = subprocess.PIPE)
	
	if os.path.isfile("{}personnal_data.tmp".format(path)):
		subprocess.run('''rm {}personnal_data.tmp'''.format(path)  , shell = True, stdout = subprocess.PIPE)
	
	if os.path.isfile("{}query.tmp".format(path)):
		subprocess.run('''rm {}query.tmp'''.format(path)           , shell = True, stdout = subprocess.PIPE)


