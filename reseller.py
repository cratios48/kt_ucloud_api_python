#! /usr/bin/python3

from basic import Basic
import json

class Reseller(Basic):

    def __init__(self, zone, apikey, secretkey):
        super().__init__(zone, 'server', apikey, secretkey)

    def list(self):
        result = self.push({'command': 'listVirtualMachines'})

        print('ZONE, NAME, TEMPLATE, IPs, PUBLIC IP, CREATED, CPU, MEMORY')
        for vm in result['listvirtualmachineresponse']['virtualmachine']:
            ipList = ''
            zone = vm.get('zonename')
            name = vm.get('displayname')
            template = vm.get('templatedisplaytext')
            publicip = vm.get('publicip')
            created = vm.get('created')
            cpu = vm.get('cpunumber')
            mem = int(vm.get('memory')) / 1024
            for nicNum in range(len(vm['nic'])):
                ipList += vm['nic'][nicNum]['ipaddress'] + ' '
            
            print(zone, name, template, ipList, publicip, created, cpu, mem, sep = ', ')