import  requests
import json

S1_HOST = 'https://apse1-2001.sentinelone.net'

suri = '/web/api/v2.1/dv/events/pq'


data = {
    "data": {
        "columns": [],
        "data": [],
        "externalId": "{\"lrqToken\":\"52800941-a1a7-4e9f-a17b-480d5ef97fea\",\"target\":\"__E1__myd7Lr_ZWiY1ucyJC8jqvShna_DrPxWO5_SDVSY9TQw-\"}",
        "progress": 45,
        "queryId": "pq2b3429c11531c3f9376566beb6b1bf09",
        "recommendations": [],
        "status": "RUNNING"
    }
}

headers = {'Content-type': 'application/json'}

url = S1_HOST + suri
response = requests.post(url, data=json.dumps(data), headers=headers)

print(response.status_code)
print(response.json())