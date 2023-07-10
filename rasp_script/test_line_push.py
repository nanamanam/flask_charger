import requests
from os import system
import time
try:
        
    data={"group_id":0,"message":"test line push"}
    res=requests.post('https://charger-3a8c5.as.r.appspot.com/api/line_push',auth=('charger_api','12312312388'),json=data)
    print(res.status_code)
    time.sleep(20)
except Exception as e:
    print('this is error')
    print(e)
    time.sleep(10)
