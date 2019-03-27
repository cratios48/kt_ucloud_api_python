#! /usr/bin/python3
"""
To encrypt small data.
Fernet is in-memory encrypt-decrypt module.
Encrypt target data as small as possible.
"""
# To use download cryptography module ex) python -m pip install cryptography
from cryptography.fernet import Fernet
import hashlib, secrets, base64
import json
#import getpass

class CloudKey():
    fileName = ''
    hashKey = ''
    keyInfo = {
        'zone': None,
        'apikey': None,
        'secretkey': None
    }

    def __init__(self, password, filename = 'key.enc'):
        """
        Instance must have hashed key and encrypted file name.
        """
        self.setHashKey(password)
        self.fileName = filename

    def keyStore(self, zone = None, apikey = None, secretkey = None):
        if zone:
            self.keyInfo['zone'] = zone
        if apikey:
            self.keyInfo['apikey'] = apikey
        if secretkey:
        #    secretkey = getpass.getpass(prompt="Secret Key: ")
            self.keyInfo['secretkey'] = secretkey

    def jsonStr(self):
        return str(self.keyInfo).replace("'","\"")
        
    def setHashKey(self, password):
        self.hashKey = hashlib.sha256(password.encode()).digest()

    def cusEnc(self):
        tokenkey = Fernet(base64.urlsafe_b64encode(self.hashKey))
        return tokenkey.encrypt(self.jsonStr().encode())

    def cusDec(self, encStr):
        tokenkey = Fernet(base64.urlsafe_b64encode(self.hashKey))
        return tokenkey.decrypt(encStr).decode()

    def fileDump(self):
        with open(self.fileName, 'wb') as fp:
            fp.write(self.cusEnc())

    def fileLoad(self):
        with open(self.fileName, 'rb') as fp:
            self.keyInfo = json.loads(self.cusDec(fp.read()))