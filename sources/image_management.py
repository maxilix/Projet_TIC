#!/usr/bin/python3


import subprocess
import pyqrcode
from PIL import Image




def create_texte_image(path, name, firstName, entitle):
	textFileName = "text_image.png"
	cmd = subprocess.Popen('''curl -o {3} "http://chart.apis.google.com/chart" --data-urlencode "chst=d_text_outline" --data-urlencode "chld=000000|56|h|FFFFFF|b|Certificat de {0}|délivré à|{1} {2}"'''.format(entitle, firstName, name, path+textFileName), shell=True, stdout=subprocess.PIPE)
	cmd.communicate()
	cmd = subprocess.Popen('''mogrify -resize 1000x600 {0}'''.format(path+textFileName), shell=True, stdout=subprocess.PIPE)
	cmd.communicate()
	return textFileName




def create_qrcode_image(path, data):
	qrcodeFileName = "qrcode_image.png"
	qr = pyqrcode.create(data, error='H', version=10)
	qr.png(path+qrcodeFileName, scale=2)
	cmd = subprocess.Popen('''mogrify -resize 210x210 {0}'''.format(path+qrcodeFileName), shell=True, stdout=subprocess.PIPE)
	cmd.communicate()
	return qrcodeFileName




def create_assembled_stegano_image(path, name, firstName, entitle, steganoMessage, qrcodeData):

	textFileName = create_texte_image(path, name, firstName, entitle)

	#f=open(path+"query.tsq",'rb')
	#qrcodeData=f.readline()
	#print(qrcodeData)
	#f.close()
	qrcodeFileName = create_qrcode_image(path,qrcodeData)

	cmd = subprocess.Popen('''composite -gravity center {0}{1} ../ressources/background.png {0}before_stegano.png'''.format(path,textFileName), shell=True, stdout=subprocess.PIPE)
	cmd.communicate()

	beforeSteganoImage = Image.open("{0}before_stegano.png".format(path))
	cacher(beforeSteganoImage, steganoMessage)
	beforeSteganoImage.save("{0}after_stegano.png".format(path))

	cmd = subprocess.Popen('''composite -geometry +1418+934 {0}{1} {0}after_stegano.png {0}certificate.png'''.format(path,qrcodeFileName), shell=True, stdout=subprocess.PIPE)
	cmd.communicate()

	cmd = subprocess.Popen('''rm {0}before_stegano.png {0}after_stegano.png {0}{1} {0}{2}'''.format(path, textFileName,qrcodeFileName), shell=True, stdout=subprocess.PIPE)
	cmd.communicate()




def decode_qrcode(certificateFileName):
	certificate = Image.open(certificateFileName)
	qrImage = certificate.crop((1418,934,1418+210,934+210))
	qrImage.save("qrcoderecupere.png", "PNG")
	cmd = subprocess.Popen('''python2 qrtools_py2.py''', shell=True, stdout=subprocess.PIPE)
	(result, ignored) = cmd.communicate()
	cmd = subprocess.Popen('''rm qrcoderecupere.png''', shell=True, stdout=subprocess.PIPE)
	cmd.communicate()
	return str(result)[2:-3]




def check_identity_images(path, fileName1, fileName2):
	
	im1 = Image.open(path+fileName1)
	im2 = Image.open(path+fileName2)

	im1Data = list(im1.getdata())
	im2Data = list(im2.getdata())

	for i in range(len(im1Data)):
		if (i%1753 < 1418 or i%1753 > 1628 or i//1753 < 934 or i//1753 > 1144):
			if (im1Data[i] != im2Data[i]):
				return False
	return True





def vers_8bit(c):
	chaine_binaire = bin(ord(c))[2:]
	return "0"*(8-len(chaine_binaire))+chaine_binaire

def modifier_pixel(pixel, bit):
	# on modifie que la composante rouge
	r_val = pixel[0]
	rep_binaire = bin(r_val)[2:]
	rep_bin_mod = rep_binaire[:-1] + bit
	r_val = int(rep_bin_mod, 2)
	return tuple([r_val] + list(pixel[1:]))

def recuperer_bit_pfaible(pixel):
	r_val = pixel[0]
	return bin(r_val)[-1]

def cacher(image,message):
	dimX,dimY = image.size
	im = image.load()
	message_binaire = ''.join([vers_8bit(c) for c in message])
	posx_pixel = 0
	posy_pixel = 0
	for bit in message_binaire:
		im[posx_pixel,posy_pixel] = modifier_pixel(im[posx_pixel,posy_pixel],bit)
		posx_pixel += 1
		if (posx_pixel == dimX):
			posx_pixel = 0
			posy_pixel += 1
		assert(posy_pixel < dimY)

def recuperer(image,taille):
	message = ""
	dimX,dimY = image.size
	im = image.load()
	posx_pixel = 0
	posy_pixel = 0
	for rang_car in range(0,taille):
		rep_binaire = ""
		for rang_bit in range(0,8):
			rep_binaire += recuperer_bit_pfaible(im[posx_pixel,posy_pixel])
			posx_pixel +=1
			if (posx_pixel == dimX):
				posx_pixel = 0
				posy_pixel += 1
		message += chr(int(rep_binaire, 2))
	return message
