#! /usr/bin/python3

from time import sleep
import server

zone = ''
apikey = ''
secretkey = ''

targetSs = server.Snapshot(zone, apikey, secretkey)
targetVol = server.Volume(zone, apikey, secretkey)

# KT Volume dislplay name list
targetVolList = []

for volume in targetVolList:
    targetSs.create(targetVol.checkId(volume))
    # To avoid error while create multiple snapshot concurrently
    sleep(300)