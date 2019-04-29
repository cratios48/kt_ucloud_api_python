#! /usr/bin/python3

from basic import Basic
from time import sleep
from server import Vm
import json

class LB(Basic):

    def __init__(self, zone, apiKey, secretKey):
        Basic.__init__(self, zone, 'loadbalancer', apiKey, secretKey)

    def listsRaw(self):
        resultJson = self.push({'command': 'listLoadBalancers'})
        return json.dumps(resultJson, indent=4, sort_keys=True)

    def lists(self):
        resultJson = self.push({'command': 'listLoadBalancers'})
        resultFormat = '{zone},{name},{ip},{port},{type},{option},{state},{hctype},{hcurl},{cert}\n'
        
        try:
            result = resultFormat.format(zone = 'ZONE', name = 'NAME', ip = 'IP', 
                                            port = 'PORT', type = 'TYPE', option = 'option', 
                                            state = 'state', hctype = 'Health Check Type', 
                                            hcurl = 'Health Check URL', cert = 'Certification') 
            for lb in resultJson['listloadbalancersresponse']['loadbalancer']:
                result += resultFormat.format(
                    zone = lb.get('zonename'),
                    name = lb.get('name'),
                    ip = lb.get('serviceip'),
                    port = lb.get('serviceport'),
                    type = lb.get('servicetype').upper(),
                    option = lb.get('loadbalanceroption'),
                    state = lb.get('state'),
                    hctype = lb.get('healthchecktype').upper(),
                    hcurl = lb.get('healthcheckurl'),
                    cert = lb.get('certificatename')
                )
        except:
            return result
        
        return result

    def listsRawResource(self):
        lbNameList = []
        resourceList = []

        try:
            resultJson = self.push({'command': 'listLoadBalancers'})
            for lb in resultJson['listloadbalancersresponse']['loadbalancer']:
                lbNameList.append(lb.get('loadbalancerid'))
    
            for lbName in lbNameList:
                resultJson = self.push({'command': 'listLoadBalancerWebServers', 'loadbalancerid': lbName})
    
                resourceList.append(resultJson)
                # Too fast API query, then Rate Limit error occur
                sleep(3)
        except:
            return resourceList

        return resourceList

    def listsReosource(self):
        lbVm = Vm(self.zone, self.api_key, self.secret_key)
        lbList = []
        vmIdList = {}
        resultFormat = '{lb},{server},{ip},{port}\n'

        try:
            result = resultFormat.format(lb = 'LB', server = 'SERVER', ip = 'IP', port = 'PORT')
            for vm in json.loads(lbVm.listsRaw())['listvirtualmachinesresponse']['virtualmachine']:
                vmIdList[vm.get('id')] = vm.get('displayname')

            resultJson = self.push({'command': 'listLoadBalancers'})
            for lb in resultJson['listloadbalancersresponse']['loadbalancer']:
                lbList.append([lb.get('loadbalancerid'), lb.get('name')])
    
            for lb in lbList:
                resultJson = self.push({'command': 'listLoadBalancerWebServers', 'loadbalancerid': lb[0]})
                for webServer in resultJson['listloadbalancerwebserversresponse']['loadbalancerwebserver']:
                    result += resultFormat.format(
                        lb = lb[1],
                        server = vmIdList[webServer.get('virtualmachineid')],
                        ip = webServer.get('ipaddress'),
                        port = webServer.get('publicport')
                    )
                sleep(3)
        except:
            return result
        
        return result