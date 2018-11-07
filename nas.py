#! /usr/bin/python3

from basic import Basic
import json
import datetime

class Nas(Basic):

    def __init__(self, zone, apikey, secretkey):
        super().__init__(zone, 'nas', apikey, secretkey)

    def rawListNas(self):
        resultJson = self.push({'command': 'listVolumes'})
        return json.dumps(resultJson, indent = 4, sort_keys = True)

    def listNas(self):
        resultJson = self.push({'command': 'listVolumes'})
        resultFormat = '{name},{type},{ip},{path},{size},{status},{created},{autoresize}\n'

        try:
            result = resultFormat.format(name = 'NAME', type = 'TYPE', ip = 'IP', path = 'PATH', size = 'SIZE', status = 'STATUS', created = 'CREATED', autoresize = 'AUTO RESIZE')
            for nas in resultJson['listvolumesresponse']['response']:
                result += resultFormat.format(
                    name = nas.get('name'),
                    volumeType = nas.get('volumetype'),
                    ip = nas.get('ip'),
                    path = nas.get('path'),
                    size = int(nas.get('totalsize'))/(1024**3),
                    status = nas.get('status'),
                    created = datetime.datetime.strptime(nas.get('created'), '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'),
                    autoResize = nas.get('autoresize')
                )
        except:
            return result

        return result