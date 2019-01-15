#! /usr/bin/python3

import os
import json
import server

with open(os.path.abspath(os.path.dirname(__file__)) + './key.json', 'r') as f:
    keyInfo = json.load(f)

zone = keyInfo['key']['zone']
apikey = keyInfo['key']['apikey']
secretkey = keyInfo['key']['secretkey']

targetVol = server.Volume(zone, apikey, secretkey)

print(targetVol.lists())