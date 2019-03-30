#!/usr/bin/python3


import subprocess
import pyqrcode
from PIL import Image




def create_texte_image(firstname,name, texteFileName):
	cmd = subprocess.Popen('''curl -o {2} "http://chart.apis.google.com/chart" --data-urlencode "chst=d_text_outline" --data-urlencode "chld=000000|56|h|FFFFFF|b|Certificat délivré|à|{0} {1}"'''.format(firstname,name,texteFileName), shell=True, stdout=subprocess.PIPE)
	cmd.communicate()
	cmd = subprocess.Popen('''mogrify -resize 1000x600 {0}'''.format(texteFileName), shell=True, stdout=subprocess.PIPE)
	cmd.communicate()


def create_qrcode_image(data,qrcodeFileName):
	qr = pyqrcode.create(data)
	qr.png("{}".format(qrcodeFileName), scale=2)
	cmd = subprocess.Popen('''mogrify -resize 210x210 {0}'''.format(qrcodeFileName), shell=True, stdout=subprocess.PIPE)
	cmd.communicate()


def create_assembled_image(texteFileName, qrcodeFileName, backgroundFileName):
	cmd = subprocess.Popen('''composite -gravity center {0} {1} temp.png'''.format(texteFileName,backgroundFileName), shell=True, stdout=subprocess.PIPE)
	cmd.communicate()
	cmd = subprocess.Popen('''composite -geometry +1418+934 {0} temp.png certificate.png'''.format(qrcodeFileName), shell=True, stdout=subprocess.PIPE)
	cmd.communicate()
	cmd = subprocess.Popen('''rm temp.png {0} {1}'''.format(texteFileName,qrcodeFileName), shell=True, stdout=subprocess.PIPE)
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




#name = input("Nom : ")
#firstname = input("Prénon : ")
texteFileName = "tt"
qrcodeFileName = "qq"

create_texte_image("Morgane","Vollmer",texteFileName)
create_qrcode_image("https://p-fb.net/fileadmin/SecuTIC/2018_2019/Securite_TIC_Projet_2018-2019.pdf",qrcodeFileName)
create_assembled_image(texteFileName,qrcodeFileName,"background.png")
print("\n\n"+ decode_qrcode("certificate.png"))


