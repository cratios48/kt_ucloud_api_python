#! /usr/bin/python3

from time import sleep
import os
import json
import server

with open(os.path.abspath(os.path.dirname(__file__)) + '/key.json', 'r') as f:
    keyInfo = json.load(f)

targetSs = server.Snapshot(**keyInfo)
targetVol = server.Volume(**keyInfo)

# KT Volume dislplay name list
targetVolList = []

for volume in targetVolList:
    targetSs.create(targetVol.checkId(volume))
    # To avoid error while create multiple snapshot concurrently
    sleep(300)