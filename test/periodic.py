import urllib.request
import json


uid1 = 'cdfd2609-e7aa-4dff-af50-649a89bd8805'
body = [{"uid": uid1, "file_name": "saurabh.py", "start_date": "2020-09-26 16:15:00", "end_date": "2020-09-26 19:00:00", "file_type": "python"}]
body1 = json.dumps(body).encode('utf-8')
code = 200
# r = requests.post('http://152.46.17.237:8080/send', json=body1)
req = urllib.request.Request("http://152.46.17.237:8080/send", data=body1, headers={'content-type': 'application/json'})
response = urllib.request.urlopen(req)
code1 = response.getcode()
assert code1 == 200
