#! /usr/bin/python3

from basic import Basic
from time import sleep
import json

class Waf(Basic):

    def __init__(self, zone, apikey, secretkey):
        super().__init__(zone, 'waf', apikey, secretkey)

    def listsRaw(self):
        resultJson = self.push({'command': 'listWAFs'})
        return json.dumps(resultJson, indent=4, sort_keys=True)

    def lists(self):
        resultJson = self.push({'command': 'listWAFs'})
        resultFormat = '{name},{zone},{ip},{port},{spec},{wafType},{active}\n'

        try:
            result = resultFormat.format(name = 'NAME', zone = 'ZONE', ip = 'IP', port = 'PORT', spec = 'SPEC', wafType = 'TYPE', active = 'ACTIVE STATE')
            for waf in resultJson['listwafsresponse']['wafservice']:
                result += resultFormat.format(
                    name = waf.get('name'),
                    active = waf.get('active'),
                    ip = waf.get('serviceip'),
                    port = waf.get('serviceport'),
                    spec = waf.get('spec'),
                    wafType = waf.get('type'),
                    zone = waf.get('zonename')
                )
        except:
            return result

        return result

    def listsRawWebservers(self):
        wafList = []
        
        try:
            resultJson = self.push({'command': 'listWAFs'})
            for waf in resultJson['listwafsresponse']['wafservice']:
                wafList.append(waf.get('id'))
    
            webserverList = []
            for waf in wafList:
                resultJson = self.push({'command': 'listWAFWebServers', 'id': waf})
                webserverList.append(resultJson)
                sleep(3)
        except:
            return None

        return webserverList

    def listsWebservers(self):
        wafList = []
        resultFormat = '{waf},{proxyport},{serverport},{ssl}\n'
        
        try:
            result = resultFormat.format(waf = 'WAF', proxyport = 'PROXY PORT', serverport = 'Web Server Port', ssl = 'SSL')
            resultJson = self.push({'command': 'listWAFs'})
            for waf in resultJson['listwafsresponse']['wafservice']:
                wafList.append([waf.get('name'), waf.get('id')])
            
            for waf in wafList:
                resultJson = self.push({'command': 'listWAFWebServers', 'id': waf[1]})
                for webServer in resultJson['listwafwebserversresponse']['webserver']:
                    result += resultFormat.format(
                        waf = waf[0],
                        proxyPort = webServer.get('proxyport1'),
                        webServerPort = webServer.get('webserverport'),
                        ssl = webServer.get('sslmode')
                    )
                sleep(3)
        except:
            return result
        
        return result