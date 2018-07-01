#! /usr/bin/env python3

import hashlib
import hmac
import base64
import requests
from xml.etree.ElementTree import parse as xp
class basic():
    KT_API_URL="https://api.ucloudbiz.olleh.com/SERVICE/VERSION/client/api?"
    SERVICE=("server",              # 서버 
                "loadbalancer",     # 로드밸런서
                "nas",              # NAS
                "cdn",              # CDN
                "autoscaling",      # 오토스케일링
                "waf",              # WAF
                "db",               # DB
                "messaging",        # 메시징
                "packaging",        # 패키징
                "watch",            # 모니터링
                "gslb"              # GSLB
    )
    API_KEY=""
    SECRET_KEY=""
    
    def sign(self, COMM):
        # URL 순서를 필요한 대로 정리한다.
        NEW_COMM = COMM.replace(" ", "+").split("&")
        NEW_COMM.sort()
        NEW_COMM = "&".join(NEW_COMM)
    
        # URL을 필요한 대로 암호화한다.
        key = bytes(self.SECRET_KEY, 'UTF-8')
        message = bytes(NEW_COMM, 'UTF-8')
    
        sign_before = hmac.new(key, message, hashlib.sha1).digest()
        sign_mid = base64.urlsafe_b64encode(sign_before)
        
        return str(sign_mid, 'UTF-8')
    
    def push(self, zone, service, comm):
        zone = zone.lower()
        service = service.lower()
    
        VERSION = 'v1'
        SERVICE = service
    
        if zone == 'm2':
            VERSION = 'v2'
        elif zone == 'gov':
            SERVICE = 'g' + service
            VERSION = 'v1'        
        else:
            print("Default is server/v1")
    
        KT_API_URL = self.KT_API_URL.replace('VERSION', VERSION)
        KT_API_URL = KT_API_URL.replace('SERVICE', SERVICE)
        
        api_response = requests.get(KT_API_URL + comm + self.sign(comm))

        if api_response.status_code != 200:
            return False
        
        return api_response.text