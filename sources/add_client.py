#!/usr/bin/python3

import base64
import subprocess

clientName = input(" - New client name : ")
clientState = input(" - New client state : ")
clientCountry = clientState[:2].upper()
clientLocality = input(" - New client city : ")
clientEmail = input(" - New client email : ")
clientPassphrase = input(" - New client passphrase : ")
clientPassphraseB32 = str(base64.b32encode(clientPassphrase.encode('UTF-8')))[2:-1]
path = "../clients/" + clientName.replace(' ','-') + "/"



# update database
f = open('../clients/clients_database', 'a')
f.write(clientName + '\t' + clientPassphraseB32 + '\t' + clientEmail + '\n')
f.close()

# make client direrectory
subprocess.run('''mkdir {0}'''.format(path), shell=True, stdout=subprocess.PIPE)

# make client bikey
subprocess.run('''openssl ecparam -out {0}ca.key -name prime256v1 -genkey'''.format(path), shell=True, stdout=subprocess.PIPE)
subprocess.run('''openssl ec -in {0}ca.key -pubout -out {0}public.ca.key'''.format(path), shell=True, stdout=subprocess.PIPE)

# make client CA
subprocess.run('''openssl req -new -config ../ressources/ca.cnf -nodes -subj "/C={2}/ST={3}/L={4}/O={1}/CN={1} CA/emailAddress={5}" -x509 -extensions ext -sha256 -key {0}ca.key -out {0}ca.cert.pem'''.format(path, clientName, clientCountry, clientState, clientLocality, clientEmail), shell=True, stdout=subprocess.PIPE)




