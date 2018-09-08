#! /usr/bin/python3

import sys

sys.path.append('../')

from basic import Basic
import json

class LB(Basic):

    def __init__(self, zone, apiKey, secretKey):
        super().__init__(zone, 'loadbalancer', apiKey, secretKey)

    def list(self):
        result = self.push({'command': 'listLoadBalancers'})
        
        print('ZONE', 'NAME', 'IP', 'PORT', 'TYPE', 'HealthCheckType'. 'HealthChckeURL', 'STATE', 'Certificate')
        for lb in result:
