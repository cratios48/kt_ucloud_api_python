#! /usr/bin/env python3

import sys

sys.path.append('../')

from basic import Basic
import xml.etree.ElementTree as ET

class Volume(Basic):

    def __init__(self, zone, apikey, secretkey):
        super().__init__(zone, apikey, secretkey)
    
    def list(self):
        rawList = self.push('server', {'command': 'listVolumes'})

        listRoot = ET.fromstring(rawList)

        print('zone, name, vmname, type, size, created')
        for volume in listRoot.findall('volume'):
            zone = volume.find('zonename').text
            name = volume.find('name').text
            vmname = volume.find('vmdisplayname').text
            vmtype = volume.find('provisioningtype').text
            size = str(int(volume.find('size').text)/(1024*1024*1024)) + ' GB'
            created = volume.find('created').text
            print(zone, name, vmname, vmtype, size, created, sep=', ')

    def checkId(self, volumeName):
        rawList = self.push('server', {'command': 'listVolumes'})

        listRoot = ET.fromstring(rawList)
        
        for volume in listRoot.findall('volume'):
            if volume.find('name').text == volumeName:
                return volume.find('id').text