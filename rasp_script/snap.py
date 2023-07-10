import requests
from os import system
from bs4 import BeautifulSoup
import time
import json

def snap():
        item={}
        url_list=[
                'http://192.168.0.10/set_system.php',
                'http://192.168.0.10/set_charging.php',
                'http://192.168.0.10/set_backend.php'
        ]
        try:
                for url in url_list:
                        res=requests.post(url,auth=('admin','1231231238'),verify=False)
                        soup = BeautifulSoup(res.content, 'html.parser')
                        print(res.status_code)
#                       print(soup.prettify())
                        select_tag=soup.find_all('select')
                        for i in select_tag:
                                opt=i.find_all('option',selected=True)[0]['value']
                                #print(i['id'],opt)
                                item[i['id']]=opt
                        input=soup.find_all('input')
                        for i in input:
                                try:
                                        item[i['id']]=i['value']
                                except Exception as e:
                        #               print(e)
                                        pass
                return json.dumps(item)
        except Exception as e:
                print('this is error')
                print(e)
print(snap())
#snap()
