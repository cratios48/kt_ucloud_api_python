#! /usr/bin/env python3

import hashlib
import hmac
import base64
from urllib.parse import urlencode
import requests
import json

class Basic():
    KT_API_URL='https://api.ucloudbiz.olleh.com/SERVICE/VERSION/client/api?'
    ZONE = ''
    VERSION = 'v1'
    SERVICE = ''
    serviceList=('server',          # 서버 
                'loadbalancer',     # 로드밸런서
                'nas',              # NAS
                'cdn',              # CDN
                'autoscaling',      # 오토스케일링
                'waf',              # WAF
                'db',               # DB
                'messaging',        # 메시징
                'packaging',        # 패키징
                'watch',            # 모니터링
                'gslb'              # GSLB
    )

    def __init__(self, ZONE, SERVICE, API_KEY, SECRET_KEY):
        if ZONE.lower() == 'm2':
            self.VERSION = 'v2'
        elif ZONE.lower() == 'gov':
            self.SERVICE = 'g'
        else:
            pass

        self.ZONE = ZONE
        self.SERVICE += SERVICE
        self.KT_API_URL = self.KT_API_URL.replace('VERSION', self.VERSION)
        self.KT_API_URL = self.KT_API_URL.replace('SERVICE', self.SERVICE)
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
    
    def sign(self, COMM):
        # URL 순서를 필요한 대로 정리한다.
        NEW_COMM = urlencode(COMM).replace('+', '%20').lower()
        NEW_COMM = '&'.join(sorted(NEW_COMM.split('&')))
    
        # URL을 필요한 대로 암호화한다.
        key = bytes(self.SECRET_KEY, 'UTF-8')
        message = bytes(NEW_COMM, 'UTF-8')
    
        sign1 = hmac.new(key, message, hashlib.sha1).digest()
        sign2 = base64.b64encode(sign1)
        
        return str(sign2, 'UTF-8')
    
    def push(self, comm):
        comm['response'] = 'json'
        comm['apiKey'] = self.API_KEY
        comm['signature'] = self.sign(comm)
        
        try:
            api_response = requests.get(self.KT_API_URL + urlencode(comm))
            result = json.loads(api_response.text)
        except requests.exceptions.RequestException as e:
            print(e)
            return None

        return result