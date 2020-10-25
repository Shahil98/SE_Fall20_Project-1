import platform
import os
import requests

if platform.system() == 'Windows':
    DATA_FOLDER_PATH = os.path.join(os.getenv('APPDATA'), 'codeTime')
else:
    DATA_FOLDER_PATH = os.path.join(os.path.expanduser('~'), 'codeTime')

if not os.path.exists(DATA_FOLDER_PATH):
    os.makedirs(DATA_FOLDER_PATH)

try:
    f = open(DATA_FOLDER_PATH+"\\userid.txt", "r")
    f.close()
except:
    print("Exception occured")
    f = open(DATA_FOLDER_PATH+"\\userid.txt", "w+")
    user_id_json = requests.get("http://152.46.17.237:8080/signup")
    user_id_json = user_id_json.json()
    f.write(user_id_json["your_id"])
    f.close()
