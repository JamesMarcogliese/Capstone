#!/usr/bin/python

import requests
import json
import sys
time = sys.argv[1]
status = sys.argv[2]
user = sys.argv[3]

url = "https://baas.kinvey.com/appdata/kid_byTiDtLe8/updates/547b998c5aee6ffe36015eb9"
payload = {"userId": user,"deviceId": "0001","status": status,"estTime": time}
headers = {"content-type": "application/json","X-Kinvey-API-Version": "3","Authorization": "Basic a2lkX2J5VGlEdExlODphYzcwMjdhOGJmMTE0N2Q4OWVlN2UwZWFiMDgxNzIxZA=="}

r = requests.put(url, data=json.dumps(payload), headers=headers)
print r.json()
