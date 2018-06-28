#! /usr/bin/env python3

import hashlib
import hmac
import base64

KT_API_URL="https://api.ucloudbiz.olleh.com/DEF/v1/client/api?"
SERVICE={"server",              # 서버 
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
}
API_KEY=""
SECRET_KEY=""

def sign(COMM):
    # URL 순서를 필요한 대로 정리한다.
    NEW_COMM = COMM.replace(" ", "+").split("&")
    NEW_COMM.sort()
    NEW_COMM = "".join(NEW_COMM)

    # URL을 필요한 대로 암호화한다.
    key = bytes(SECRET_KEY, 'UTF-8')
    message = bytes(NEW_COMM, 'UTF-8')

    sign_before = hmac.new(key, message, hashlib.sha1).digest()
    sign_mid = base64.urlsafe_b64decode(sign_before)
    
    return str(sign_mid, 'UTF-8')

def push(zone, service, comm):