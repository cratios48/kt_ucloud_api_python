#! /usr/bin/python3

import server

zone = ''
apikey = ''
secretkey = ''

targetSs = server.Snapshot(zone, apikey, secretkey)

print(targetSs.listSnapshot())