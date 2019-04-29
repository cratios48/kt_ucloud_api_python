#! /usr/bin/env python3
"""
KT uCloud Open API basic function
"""
import hashlib
import hmac
import base64
from urllib.parse import urlencode
import requests
import json

class Basic():
    """
    KT uCloud service list
    - server
    - loadbalancer
    - nas
    - cdn
    - autoscaling
    - waf
    - db
    - messaging
    - packaging
    - watch
    - gslb
    """
    kt_api_url='https://api.ucloudbiz.olleh.com/{service}/{version}/client/api?'

    def __init__(self, zone, service, api_key, secret_key):
        version = 'v1'
        if zone.lower() == 'm2':
            version = 'v2'
        elif zone.lower() == 'gov':
            service = 'g' + service
        self.zone = zone
        self.kt_api_url = self.kt_api_url.format(service = service, version = version)
        self.api_key = api_key
        self.secret_key = secret_key
    
    def sign(self, comm):
        # Reorder URL path as needed
        new_comm = urlencode(comm).replace('+', '%20').lower()
        new_comm = '&'.join(sorted(new_comm.split('&')))
    
        # Encrypt URL
        key = bytes(self.secret_key, 'UTF-8')
        message = bytes(new_comm, 'UTF-8')
    
        sign1 = hmac.new(key, message, hashlib.sha1).digest()
        sign2 = base64.b64encode(sign1)
        
        return str(sign2, 'UTF-8')
    
    def push(self, comm):
        comm['response'] = 'json'
        comm['apiKey'] = self.api_key
        comm['signature'] = self.sign(comm)
        
        try:
            api_response = requests.get(self.kt_api_url + urlencode(comm))
            result = json.loads(api_response.text)
        except requests.exceptions.RequestException as e:
            print(e)
            return None

        return result