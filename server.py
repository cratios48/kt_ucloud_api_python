#! /usr/bin/python3

from basic import Basic
import xml.etree.ElementTree as ET

class Server(Basic):

    def __init__(self, zone, apikey, secretkey):
        super().__init__(zone, apikey, secretkey)

    def list(self):
        rawList = self.push('server', {'command': 'listVirtualMachines'})

        listRoot = ET.fromstring(rawList)

        print('ZONE, NAME, TEMPLATE, IPs, PUBLIC IP, CREATED')
        for server in listRoot.findall('virtualmachine'):
            ips = ''
            for nic in server.findall('nic'):
                ips += nic.find('ipaddress') + ' '
            zone = server.find('zonename').text
            name = server.find('displayname').text
            template = server.find('template').text
            publicip = server.find('publicip').text
            created = server.find('created').text
            print(zone, name, template, ips, publicip, created, sep=', ')

