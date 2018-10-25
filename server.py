#! /usr/bin/python3

from basic import Basic
import json
import time
import datetime

class Vm(Basic):

    def __init__(self, zone, apikey, secretkey):
        super().__init__(zone, 'server', apikey, secretkey)

    def rawList(self):
        resultJson = self.push({'command': 'listVirtualMachines'})
        return json.dumps(resultJson, indent = 4, sort_keys = True)

    def list(self):
        resultJson = self.push({'command': 'listVirtualMachines'})
        resultFormat = '{zone},{name},{template},{ip},{publicip},{cpu},{mem},{created}\n'

        try:
            result = resultFormat.format(zone='ZONE', name='NAME', template='TEMPLATE', ip='IPs', publicip='PUBLIC IP', cpu='CPU', mem='MEMORY', created='CREATED')
            for vm in resultJson['listvirtualmachinesresponse']['virtualmachine']:
                ipList = ''
                for nicNum in range(len(vm['nic'])):
                    ipList += vm['nic'][nicNum]['ipaddress'] + ' '
                ipList = ipList[:-1]
                result += resultFormat.format(
                    zone = vm.get('zonename'),
                    name = vm.get('displayname'),
                    template = vm.get('templatedisplaytext'),
                    ip = ipList,
                    publicip = vm.get('publicip'),
                    created = datetime.datetime.strptime(vm.get('created'), '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S'),
                    cpu = vm.get('cpunumber'),
                    mem = int(vm.get('memory')) / 1024
                )
        except:
            return result

        return result

class Volume(Basic):

    def __init__(self, zone, apikey, secretkey):
        super().__init__(zone, 'server', apikey, secretkey)
    
    def rawList(self):
        resultJson = self.push({'command': 'listVolumes'})
        return json.dumps(resultJson, indent = 4, sort_keys = True)

    def list(self):
        resultJson = self.push({'command': 'listVolumes'})
        resultFormat = '{zone},{name},{vmname},{vmtype},{size},{created}\n'

        try:
            result = resultFormat.format(zone = 'ZONE', name = 'NAME', vmname = 'VM', vmtype = 'TYPE', size = 'SIZE', created = 'CREATED')
            for volume in resultJson['listvolumesresponse']['volume']:
                result += resultFormat.format(
                    zone = volume.get('zonename'),
                    name = volume.get('name'),
                    vmname = volume.get('vmdisplayname'),
                    vmtype = volume.get('provisioningtype'),
                    size = str(int(volume.get('size'))/(1024*1024*1024)) + ' GB',
                    created = datetime.datetime.strptime(volume.get('created'), '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S'),
                )
        except:
            return result

        return result

    def checkId(self, volumeName):
        rawList = self.push({'command': 'listVolumes'})

class Snapshot(Basic):

    def __init__(self, zone, apikey, secretkey):
        super().__init__(zone, 'server', apikey, secretkey)

    def rawList(self):
        resultJson = self.push({'command': 'listSnapshots'})
        return json.dumps(resultJson, indent = 4, sort_keys = True)

    def list(self):
        resultJson = self.push({'command': 'listSnapshots'})
        resultFormat = '{volume},{name},{id},{size},{created}\n'

        try:
            result = resultFormat.format(volume = 'VOLUME', name = 'NAME', id = 'ID', size = 'SIZE', created = 'CREATED')
            for snapshot in resultJson['listsnapshotsresponse']['snapshot']:
                result += resultFormat.format(
                    volume = snapshot.get('volumename'),
                    created = datetime.datetime.strptime(snapshot.get('created'), '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d'),
                    name = snapshot.get('name'),
                    snapshotId = snapshot.get('id'),
                    size = str(round(int(snapshot.get('physicalsize'))/(1024*1024), 2)) + ' MB'
                )
        except:
            return result

        return result

    def create(self, volumeId):
        resultJson = self.push( {'command': 'createSnapshot', 'volumeid': volumeId})

        print('Job ID: ' + resultJson.get('jobid'))

    def delete(self, snapshotId):
        resultJson = self.push( {'command': 'deleteSnapshot', 'id': snapshotId})

        print('Job ID: ' + resultJson.get('jobid'))

    def checkId(self, target):
        if isinstance(target, str):
            resultJson = self.push( {'command': 'listSnapshots'})

            snapshotList = []

            for snapshot in resultJson['listsnapshotresponse']['snapshot']:
                if snapshot.get('volumename') == target:
                    snapshotList.append(snapshot.find('id').text)

            return snapshotList
        elif isinstance(target, (str, int)):
            resultJson = self.push( {'command': 'listSnapshots'})

            snapshotList = [] 

            for snapshot in resultJson['listsnapshotresponse']['snapshot']:
                if snapshot.get('volumename') == target:
                    snapshotId = snapshot.get('id')
                    snapshotCreated = snapshot.get('created')
                    snapshotList.append([snapshotId, snapshotCreated])

            return snapshotList
        else:
            print('Condition not matched.')
            return None