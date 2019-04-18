#! /usr/bin/python3

import os
import json
import server

with open(os.path.abspath(os.path.dirname(__file__)) + '/key.json', 'r') as f:
    keyInfo = json.load(f)

targetSs = server.Snapshot(**keyInfo)

print(targetSs.lists())