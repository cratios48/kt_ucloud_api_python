#! /usr/bin/python3

import os
import json
import server

with open(os.path.abspath(os.path.dirname(__file__)) + './key.json', 'r') as f:
    keyInfo = json.load(f)

zone = keyInfo['key']['zone']
apikey = keyInfo['key']['apikey']
secretkey = keyInfo['key']['secretkey']

targetSs = server.Snapshot(zone, apikey, secretkey)

print(targetSs.lists())