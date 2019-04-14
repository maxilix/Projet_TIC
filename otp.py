# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 07:52:14 2019

@author: Cirthy
"""

#import subprocess
import hashlib
import base64


def googleAuthentificatorOTPGen(secret):
    key = base64.b32decode(secret)
    print(key)
    """date  = subprocess.run('date +%s',shell=True,stdout=subprocess.PIPE) #
    print(date)"""
    date = 1553593866
    m = date // 30
    """hash = subprocess.run('openssl trucmuche', ,shell=True,stdout=subprocess.PIPE)
    print(hash)"""
    hash = '12664859463664F5DD52'
    t_hash = hash[-4:]
    #t_hash[0] = 0
    otp = str(int(t_hash, 16) % 1000000).zfill(6)
    return otp

googleAuthentificatorOTPGen(base64.b32encode('coucou'.encode('UTF-8')))