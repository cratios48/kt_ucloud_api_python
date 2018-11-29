#! /usr/bin/python3

from basic import Basic
import json
import datetime

class Vm(Basic):

    def __init__(self, zone, apikey, secretkey):
        super().__init__(zone, 'server', apikey, secretkey)

    def listsRaw(self):
        resultJson = self.push({'command': 'listVirtualMachines'})
        return json.dumps(resultJson, indent = 4, sort_keys = True)

    def lists(self):
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
    
    def listsRaw(self):
        resultJson = self.push({'command': 'listVolumes'})
        return json.dumps(resultJson, indent = 4, sort_keys = True)

    def lists(self):
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
                    size = str(int(volume.get('size'))/(1024**3)) + ' GB',
                    created = datetime.datetime.strptime(volume.get('created'), '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S'),
                )
        except:
            return result

        return result

    def checkId(self, volumeName):
        resultJson = self.push({'command': 'listVolumes'})

        for volume in resultJson['listvolumesresponse']['volume']:
            if volume.get('name') == volumeName:
                return volume.get('id')

        return None

    def serverVolume(self, server):
        resultJson = self.push({'command': 'listVolumes'})

        volList = []

        for volume in resultJson['listvolumesresponse']['volume']:
            if volume.get('vmdisplayname') == server:
                volList.append(volume.get('id'))

        return volList

class Snapshot(Basic):

    def __init__(self, zone, apikey, secretkey):
        super().__init__(zone, 'server', apikey, secretkey)

    def listsRaw(self):
        resultJson = self.push({'command': 'listSnapshots'})
        return json.dumps(resultJson, indent = 4, sort_keys = True)

    def lists(self):
        resultJson = self.push({'command': 'listSnapshots'})
        resultFormat = '{volume},{name},{id},{size},{created}\n'

        try:
            result = resultFormat.format(volume = 'VOLUME', name = 'NAME', id = 'ID', size = 'SIZE', created = 'CREATED')
            for snapshot in resultJson['listsnapshotsresponse']['snapshot']:
                result += resultFormat.format(
                    volume = snapshot.get('volumename'),
                    name = snapshot.get('name'),
                    id = snapshot.get('id'),
                    size = str(round(int(snapshot.get('physicalsize'))/(1024**2), 2)) + ' MB',
                    created = datetime.datetime.strptime(snapshot.get('created'), '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S')
                )
        except:
            return result

        return result

    def create(self, volumeId):
        resultJson = self.push( {'command': 'createSnapshot', 'volumeid': volumeId})

        return resultJson.get('jobid')

    def delete(self, snapshotId):
        resultJson = self.push( {'command': 'deleteSnapshot', 'id': snapshotId})

        return resultJson.get('jobid')

    def checkId(self, volumeName):
        resultJson = self.push({'command': 'listSnapshots'})

        snapshotList = []

        for snapshot in resultJson['listsnapshotsresponse']['snapshot']:
            if snapshot.get('volumename') == volumeName:
                snapshotList.append(snapshot.get('id'))

        return snapshotList

    def checkIdCreate(self, volumeName):
        resultJson = self.push({'command': 'listSnapshots'})

        snapshotList = []

        for snapshot in resultJson['listsnapshotsresponse']['snapshot']:
            if snapshot.get('volumename') == volumeName:
                snapshotList.append([snapshot.get('id'), snapshot.get('created')])
        
        return snapshotList