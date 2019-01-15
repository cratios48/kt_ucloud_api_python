#! /usr/bin/python3

from basic import Basic
from time import sleep
import json

class Reseller(Basic):
    resellerKey = ''

    def __init__(self, zone, apikey, secretkey, resellerkey):
        super().__init__(zone, '', apikey, secretkey)
        self.KT_API_URL='https://ucloudbiz.olleh.com/jv_ssl_key_openapi.jsp?'
        self.resellerKey = resellerkey
        if self.ZONE.lower() == 'gov':
            self.KT_API_URL = self.KT_API_URL.replace('ucloudbiz', 'gov.ucloudbiz')
        else:
            pass

    def rawListsMember(self):
        resultJson = self.push({'command': 'memberInfo', 'resellerKey': self.resellerKey})

        return json.dumps(resultJson, indent=4, sort_keys=True)

    def listsMember(self):
        resultJson = self.push({'command': 'memberInfo', 'resellerKey': self.resellerKey})

        memberList = []

        for member in resultJson['memberinforesponse']['memberids']:
            memberList.append(member.get('id'))

        return memberList

    def rawListsServiceNumber(self):
        memberList = self.listsMember()
        idList = {}
        idList['id'] = []

        for email in memberList:
            custom = self.push({'command': 'serviceNumber', 'resellerKey': self.resellerKey, 'id': email})
            idList['id'].append(custom)

        return json.dumps(idList, indent=4, sort_keys=True)

    def listsServiceNumber(self):
        memberList = self.listsMember()
        resultFormat = '{customerId},{serviceNumber}\n'

        try:
            result = resultFormat.format(customerId = 'Customer ID', serviceNumber = 'Service Number')
            for email in memberList:
                custom = self.push({'command': 'serviceNumber', 'resellerKey': self.resellerKey, 'id': email})['servicenumberresponse']
                result += resultFormat.format(
                    customerId = custom.get('emailid'),
                    serviceNumber = custom.get('servicenumber')
                )
                sleep(0.5)
        except:
            return result 

        return result

    def listsID(self, serviceNumber):
        numberList = json.loads(self.rawListsServiceNumber())
        result = 'No email has this service number - ' + serviceNumber

        for number in numberList['id']:
            if number['servicenumberresponse']['servicenumber'] == serviceNumber: 
                result = number['servicenumberresponse']['emailid']
        
        return result