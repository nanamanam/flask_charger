import requests
from os import system
import time
while True:
        try:
                with open("/home/pi/api_call/ngrok.log") as origin:
                        for line in origin:
                                if "url=http://" in line:
                                        result=str(line.split('url=')[1])
                                        if "\n" in result:
                                                final_result=result.split('\n')[0]+'/api'
                                                print(result.split('\n')[0]+'/api')
                                        else:
                                                final_result=result+'/api'
                                                print('no space')
                data={"api_path":final_result,"device_name":"device1"}
                res=requests.post('https://charger-3a8c5.as.r.appspot.com/api/update_api_path',auth=('charger_api','12312312388'),json=data)
                print(res.status_code)
                time.sleep(20)
        except Exception as e:
                print('this is error')
                print(e)
                time.sleep(10)
