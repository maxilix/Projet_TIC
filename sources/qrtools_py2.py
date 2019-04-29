#!/usr/bin/python2

import qrtools


qr = qrtools.QR()
qr.decode("qrcoderecupere.png")
print(str(qr.data))