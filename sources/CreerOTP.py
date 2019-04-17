#!/usr/bin/python3

import  subprocess
import  base64
import  random
import  os


SECRET_LENGTH = 16


def secret_generator():
    secret = ""
    for i in range(SECRET_LENGTH):
        secret += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567')
    return secret



def google_authentificator_OTP_generator(secret):
    key = base64.b32decode(secret)
    date = str(subprocess.run('date +%s',shell=True,stdout=subprocess.PIPE))
    date = date[date.find('stdout') + 9:-4]
    m = int(date) // 30
    hashMac = str(subprocess.run('echo -n {} | openssl sha1 -hmac {}'.format(date, key), shell=True, stdout=subprocess.PIPE))
    hashMac = hashMac[hashMac.find('stdout') + 18 : -4]
    truncatedHashMac = hex(int(hashMac,16) & 0x7fffffff)
    otp = str(int(truncatedHashMac, 16) % 1000000).zfill(6)
    return (date,otp)

def CreerOTP():
    name = input("Nom du propriétaire : ")
    firstName = input("Prénom du propriétaire : ")

    name=name.replace(" ","-")
    firstName=firstName.replace(" ","-")
    if (os.path.isdir("./{}_{}".format(name,firstName))):
        print("OTP déja généré.")
    else:
        subprocess.run('''mkdir {}_{}'''.format(name,firstName),shell=True,stdout=subprocess.PIPE)
        otpFile = open("./{}_{}/otp".format(name,firstName),'w')
        (date,otp) = google_authentificator_OTP_generator(secret_generator())
        otpFile.write(str(date)+'\n'+str(otp)+'\n')
        otpFile.close()

CreerOTP()