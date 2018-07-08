#! /usr/bin/env python3

import hashlib
import hmac
import base64
import requests
from xml.etree.ElementTree import parse as xp

class basic():
    KT_API_URL='https://api.ucloudbiz.olleh.com/SERVICE/VERSION/client/api?'
    SERVICE=('server',              # 서버 
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
    VERSION = 'v1'
    SERVICE = ''

    def __init__(self, TYPE, API_KEY, SECRET_KEY):
        if TYPE.lower() == 'm2':
            self.VERSION = 'v2'
        elif TYPE.lower() == 'gov':
            self.SERVICE == 'g'
        else:
            pass

        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
    
    def sign(self, COMM):
        # URL 순서를 필요한 대로 정리한다.
        NEW_COMM = COMM.lower().replace(' ', '%20').split('&')
        NEW_COMM.sort()
        NEW_COMM = '&'.join(NEW_COMM)
    
        # URL을 필요한 대로 암호화한다.
        key = bytes(self.SECRET_KEY, 'UTF-8')
        message = bytes(NEW_COMM, 'UTF-8')
    
        sign1 = hmac.new(key, message, hashlib.sha1).digest()
        sign2 = base64.b64encode(sign1)
        
        return '&signature=' + str(sign2, 'UTF-8')
    
    def push(self, service, comm):
        SERVICE = self.SERVICE + service
        COMM = comm + '&apiKey=' + self.API_KEY

        KT_API_URL = self.KT_API_URL.replace('VERSION', self.VERSION)
        KT_API_URL = KT_API_URL.replace('SERVICE', SERVICE)
        
        api_response = requests.get(KT_API_URL + COMM + self.sign(COMM))

        return api_response.text
