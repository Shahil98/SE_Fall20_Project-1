import urllib.request
import json


def tester(data):
    body1 = json.dumps(data).encode('utf-8')
    code = 200
    req = urllib.request.Request("http://152.46.17.237:8080/send", data=body1, headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(req)
    code1 = response.getcode()
    print(code1)
    return code
