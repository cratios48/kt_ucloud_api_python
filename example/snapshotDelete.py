#! /usr/bin/python3

from time import sleep
import server

zone = ''
apikey = ''
secretkey = ''

targetSs = server.Snapshot(zone, apikey, secretkey)
targetVol = server.Volume(zone, apikey, secretkey)

# Number of preserved snapshot
count = 7

targetVolList = []
targetSsList = []

for volume in targetVolList:
    tmpList = targetSs.checkIdCreate(volume)
    # Delete snapshot from oldest
    tmpList.sort(lambda a: a[1], reverse=True)
    targetSsList += tmpList
    # To avoid KT API request time limit error.
    sleep(1)

for targetSnapshot in targetSsList:
    targetSs.delete(targetSnapshot[0])
    # To avoid error while multiple snapshot deleting.
    sleep(10)