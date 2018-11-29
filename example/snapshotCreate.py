#! /usr/bin/python3

from time import sleep
import os
import json
import server

with open(os.path.abspath(os.path.dirname(__file__)) + './key.json', 'r') as f:
    keyInfo = json.load(f)

zone = keyInfo['key']['zone']
apikey = keyInfo['key']['apikey']
secretkey = keyInfo['key']['secretkey']

targetSs = server.Snapshot(zone, apikey, secretkey)
targetVol = server.Volume(zone, apikey, secretkey)

# KT Volume dislplay name list
targetVolList = []

for volume in targetVolList:
    targetSs.create(targetVol.checkId(volume))
    # To avoid error while create multiple snapshot concurrently
    sleep(300)