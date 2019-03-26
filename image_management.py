#!/usr/bin/python3


import subprocess
import pyqrcode
from PIL import Image




def create_texte_image(firstname,name):
	cmd = subprocess.Popen('''curl -o texte.png "http://chart.apis.google.com/chart" --data-urlencode "chst=d_text_outline" --data-urlencode "chld=000000|56|h|FFFFFF|b|Certificat délivré|à|{0} {1}"'''.format(firstname,name), shell=True, stdout=subprocess.PIPE)
	cmd.communicate()

def create_qrcode_image(data):
	qr = pyqrcode.create(data)
	qr.png("qrcode.png", scale=2)

def create_assembled_image():#texteFileName, qrcodeFileName, backgroundFileName):
	cmd = subprocess.Popen('''composite -gravity center texte.png background.png combinaison.png''', shell=True, stdout=subprocess.PIPE)
	cmd.communicate()
	cmd = subprocess.Popen('''composite -geometry +1418+934 qrcode.png combinaison.png attestation.png''', shell=True, stdout=subprocess.PIPE)
	cmd.communicate()

#name = input("Nom : ")
#firstname = input("Prénon : ")
create_texte_image("Morgane","Vollmer")
create_qrcode_image("https://p-fb.net/fileadmin/SecuTIC/2018_2019/Securite_TIC_Projet_2018-2019.pdf")
create_assembled_image()
