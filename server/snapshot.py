#! /usr/bin/python3

import sys

sys.path.append('../')

from basic import Basic
import xml.etree.ElementTree as ET

class Snapshot(Basic):

    def __init__(self, zone, apikey, secretkey):
        super().__init__(zone, apikey, secretkey)

    def list(self):
        rawList = self.push('server', {'command': 'listSnapshots'})

        listRoot = ET.fromstring(rawList)

        print('Volume', 'Created', 'Name', 'Size', sep=', ')
        for snapshot in listRoot.findall('snapshot'):
            volume = snapshot.find('volumename').text
            created = snapshot.find('created').text
            name = snapshot.find('name').text
            size = str(round(int(snapshot.find('physicalsize').text)/(1024*1024), 2)) + ' MB'
            print(volume, created, name, size, sep=', ')

    def create(self, volumeId):
        result = self.push('server', {'command': 'createSnapshot', 'volumeid': volumeId})

        resultRoot = ET.fromstring(result)

        print('Job ID: ' + resultRoot.find('jobid').text)

    def delete(self, snapshotId):
        result = self.push('server', {'command': 'deleteSnapshot', 'id': snapshotId})

        resultRoot = ET.fromstring(result)

        print('Job ID: ' + resultRoot.find('jobid').text)

    def checkId(self, target):
        if isinstance(target, str):
            result = self.push('server', {'command': 'listSnapshots'})

            listRoot = ET.fromstring(result)

            snapshotList = []

            for snapshot in listRoot.findall('snapshot'):
                if snapshot.find('volumename').text == target:
                    snapshotList.append(snapshot.find('id').text)

            return snapshotList
        elif isinstance(target, (str, int)):
            result = self.push('server', {'command': 'listSnapshots'})

            listRoot = ET.fromstring(result)

            snapshotList = [] 

            for snapshot in listRoot.findall('snapshot'):
                if snapshot.find('volumename').text == target:
                    snapshotId = snapshot.find('id').text
                    snapshotCreated = snapshot.find('created').text
                    snapshotList.append([snapshotId, snapshotCreated])

            return snapshotList
        else:
            print('Condition not matched.')
            return None