#! /usr/bin/python3

import sys

sys.path.append('../')

from basic import Basic
import json

class Vm(Basic):

    def __init__(self, zone, apikey, secretkey):
        super().__init__(zone, apikey, secretkey)

    def list(self):
        result = self.push('server', {'command': 'listVirtualMachines'})

        print('ZONE, NAME, TEMPLATE, IPs, PUBLIC IP, CREATED, CPU, MEMORY')
        for vm in result['listvirtualmachineresponse']['virtualmachine']:
            ipList = ''
            zone = vm.get('zonename', default = None)
            name = vm.get('displayname', default = None)
            template = vm.get('templatedisplaytext', default = None)
            publicip = vm.get('publicip', default = None)
            created = vm.get('created', default = None)
            cpu = vm.get('cpunumber', default = None)
            mem = int(vm.get('memory')) / 1024
            for nicNum in range(len(vm['nic'])):
                ipList += vm['nic'][nicNum]['ipaddress'] + ' '
            
            print(zone, name, template, ipList, publicip, created, cpu, mem, sep = ', ')