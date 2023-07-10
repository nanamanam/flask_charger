import requests
import random
import threading
import time
import config as cfg
from db import update_device,get_charger
pub_api_user=cfg.api['pub_user']
pub_api_key=cfg.api['pub_key']

def run_thread():
    data=get_charger()
    for i in data:
        threading.Thread(target=fetch_charger,args=(i['name'],)).start()
    
def fetch_charger(name):
    while True:
        try:
            data=get_charger()
            for i in data:
                if name==i['name']:
                    api_path=i['api_path']
                    res=requests.get(api_path, auth=(pub_api_user,pub_api_key))
                    print(name," : ",api_path)
            if res.status_code==200:
                update_device(res.json())
                time.sleep(5)
        except Exception as e:
            print('this is error')
            print(e)
            time.sleep(5)
def get_device():
    data = {
        "name":"device2",
        "status": 1,
        "plug1":random.randrange(0,400),
        "plug2":random.randrange(0,400)
    }
    return data