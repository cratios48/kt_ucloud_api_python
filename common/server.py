#! /usr/bin/python3

from basic import Basic
from prettytable import PrettyTable
import datetime
import json
class Vm(Basic):
    """
    Create, Delete, Modify, Search KT uCloud vm resource
    """

    def __init__(self, zone, apikey, secretkey):
        Basic.__init__(self, zone, 'server', apikey, secretkey)
        self.lastCheck = datetime.datetime.now()
        self.vmInfo = self.push({'command': 'listVirtualMachines'})

    def __repr__(self):
        self.checkInfo()
        return json.dumps(self.vmInfo, indent=4, sort_keys=True)

    def checkInfo(self):
        """
        Refresh info if last check time is more than 60 seconds ago
        """
        tmpCheck = datetime.datetime.now()

        if (tmpCheck - self.lastCheck).total_seconds() > 60:
            self.lastCheck = tmpCheck
            self.vmInfo = self.push({'command': 'listVirtualMachines'})

    def listsRaw(self):
        self.checkInfo()
        return json.dumps(self.vmInfo, indent = 4, sort_keys = True)

    def lists(self):
        self.checkInfo()
        tmpVmInfo = self.vmInfo
        resultFormat = '{zone},{name},{template},{ip},{publicip},{cpu},{mem},{created}\n'

        try:
            result = resultFormat.format(zone='ZONE', name='NAME', template='TEMPLATE', ip='IPs', publicip='PUBLIC IP', cpu='CPU', mem='MEMORY', created='CREATED')
            for vm in tmpVmInfo['listvirtualmachinesresponse']['virtualmachine']:
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

    def listsTable(self):
        resultJson = self.push({'command': 'listVirtualMachines'})
        t = PrettyTable()

        t.field_names = ['ZONE', 'NAME','TEMPLATE', 'IPs', 'PUBLIC IP', 'CPU', 'MEMORY', 'CREATED']

        for vm in resultJson['listvirtualmachinesresponse']['virtualmachine']:
            #try:
            ipList = ''
            for nicNum in range(len(vm['nic'])):
                ipList += vm['nic'][nicNum]['ipaddress'] + ' '
            ipList = ipList[:-1]
            t.add_row([
                vm.get('zonename'),
                vm.get('displayname'),
                vm.get('templatedisplaytext'),
                ipList,
                vm.get('publicip'),
                vm.get('cpunumber'),
                int(vm.get('memory')) / 1024,
                datetime.datetime.strptime(vm.get('created'), '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S')
            ])
            #except:
            #    pass

        return t

class Volume(Basic):

    def __init__(self, zone, apikey, secretkey):
        Basic.__init__(self, zone, 'server', apikey, secretkey)
    
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
        Basic.__init__(self, zone, 'server', apikey, secretkey)

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