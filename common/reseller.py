#! /usr/bin/python3

from basic import Basic
from time import sleep
import json

class Reseller(Basic):
    resellerKey = ''

    def __init__(self, zone, apikey, secretkey, resellerkey):
        Basic.__init__(self, zone, '', apikey, secretkey)
        self.kt_api_url='https://ucloudbiz.olleh.com/jv_ssl_key_openapi.jsp?'
        self.resellerKey = resellerkey
        if self.zone.lower() == 'gov':
            self.kt_api_url = self.kt_api_url.replace('ucloudbiz', 'gov.ucloudbiz')
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

    def listServiceNumber(self, email):
        comm = {}
        comm['command'] = 'serviceNumber'
        comm['resellerKey'] = self.resellerKey
        comm['id'] = email

        return self.push(comm)

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
                sleep(2)
        except:
            print("Error: API Server not respond.")
            return result 

        return result

    def listsID(self, serviceNumber):
        numberList = json.loads(self.rawListsServiceNumber())
        result = 'No email has this service number - ' + serviceNumber

        for number in numberList['id']:
            if number['servicenumberresponse']['servicenumber'] == serviceNumber: 
                result = number['servicenumberresponse']['emailid']
        
        return result

    def listCharges(self, emailid, startDate, endDate, requestType='billingInfoListAccounts'):
        comm = {}
        comm['command'] = 'listCharges'
        comm['resellerkey'] = self.resellerKey

        if emailid != '':
            comm['emailid'] = emailid

        comm['startDate'] = startDate
        comm['endDate'] = endDate
        comm['type'] = requestType

        return json.dumps(self.push(comm), indent=4, sort_keys=4)