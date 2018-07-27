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