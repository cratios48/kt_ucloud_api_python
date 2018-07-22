#! /usr/bin/env python3

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
            size = volume.find('size').text
            created = volume.find('created').text
            print(zone, name, vmname, vmtype, size, created, sep=', ')