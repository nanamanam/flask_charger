from flask import Flask, render_template, make_response,jsonify,request,session,redirect,flash,abort
import os
import json
import hashlib
import time
from get_api import fetch_charger,get_device,run_thread
from db import get_charger_detail,get_charger_config,update_api_path,update_api,get_log,check_basic_auth,approve_user,get_user,add_user,go_login,get_charger,update_charger_point,update_line_auth,get_line_auth,update_line_register,check_line_auth,get_line_group
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)
import requests
import config as cfg
from flask_sock import Sock
from flask_httpauth import HTTPBasicAuth
from bs4 import BeautifulSoup
import threading
line_api=cfg.line['line_api']
line_secret=cfg.line['line_secret']
api_user=cfg.api['user']
api_key=cfg.api['key']
line_bot_api = LineBotApi(line_api)
handler = WebhookHandler(line_secret)

app = Flask(__name__)
auth = HTTPBasicAuth()
sock = Sock(app)
# app.secret_key = os.urandom(12)
app.secret_key=cfg.app['secret_key']
def format_server_time():
  server_time = time.localtime()
  return time.strftime("%I:%M:%S %p", server_time)


def get_thread():
    while True:
        cmd=input('')
        if cmd=='c':
            print('Thread count=',threading.activeCount())
# threading.Thread(target=get_thread).start()

####Start api call from all device####

run_thread()

########threading ####################


@app.route('/web')
def web_scraper():
    url = requests.get('https://getbootstrap.com/docs/5.3/content/tables/')
    soup = BeautifulSoup(url.content, 'html.parser')
    data = soup.get_text()
    return data
    # return data.text.encode('utf-8')

@app.route('/webhook', methods=['GET','POST'])
def webhook():
	# get X-Line-Signature header value
	signature = request.headers['X-Line-Signature']
	# get request body as text
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)
	# handle webhook body
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)
	return 'Connection'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    id = event.source.user_id   #Obtaining a LINE user ID
    app.logger.info(event.message.text)
    check_status=check_line_auth(event.source.user_id)
    reply_message=""
    print("line_status=",check_status)
    print(event.message.text)
    if event.message.text == "myid":
        reply_message= event.source.user_id
    elif event.message.text == "groupid":
        reply_message= event.source.group_id 
    elif event.message.text.find("register")!=-1:   
        data=event.message.text.split('-')
        try:
            print(data[1])
            update_line_auth(data[1],1,event.source.user_id)
            reply_message='คุณได้ทำการลงทะเบียนเรียบร้อย\nกรุณา login เข้าระบบ จากนั้นจะมีปุ่ม line ขึ้นแถบด้านบนให้กดเพื่อยืนยันตัวตน'
        except Exception as e:
            print(e)
            reply_message='ขออภัย เกิดความผิดพลาดในการลงทะเบียน กรุณาลองอีกครั้ง'
    elif check_status==1:#already regis
        reply_message='กรุณา login เข้าระบบเพื่อดำเนินการต่อ'
    elif check_status==0:#nonregister
        reply_message='ขั้นตอนการลงทะเบียน LineBot\nให้ทำการพิมพ์:\nregister-[ชื่อผู้ใช้งาน]\nตัวอย่าง "register-lineuser"'       
    else:    
        if event.message.text.find("report")!=-1:
            response=get_charger()
            reply_message = ""
            for info in response:
                if info['status']==0:
                    reply_message += info['name'] + "-" + info['location'] + " (down)\n"
                elif info['status']==1:
                    reply_message += info['name'] + "-" + info['location'] + " (online)\n"
    

    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_message))

@app.route("/api/line_push",methods=['POST'])
@auth.login_required
def line_push_message():
    try:
        data=get_line_group(request.get_json()['group_id'])
        for i in data:
            if(i['line_regis']==2):
                print(i['username'])
                line_bot_api.push_message(i['line_id'], TextSendMessage(text=request.get_json()['message']))
    except Exception as e:
        return e
    return 'Push success'

@auth.verify_password
def authenticate(username, password):
    return check_basic_auth(username,password)

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/ws")
def ws():
    return render_template('web_socket.html')

@app.route("/register_access",methods = ['POST'])
def register_access():
    user=request.form['user']
    result=get_line_auth(user)
    # print(result)
    if result!=0:
        flash("Duplicate Username")
        return redirect('/register')
    else:
        if request.form['password']==request.form['confirmpassword']:
            password_key=request.form['password'].encode('utf-8')
            password_key=hashlib.sha224(password_key).hexdigest()
            # password_key=request.form['password']
            try:
                add_user(user,password_key)
                flash("Register successul")
            except Exception as e:
                print(e)
                flash("Register Error")
            return render_template('login.html')
        else:
            flash("confirm password is not match")
            return redirect('/register')

@app.route("/")
def login():
    if session.get('logged_in'):
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/api/get_charger_detail',methods=['POST'])
@auth.login_required
def got_charger_detail():
    return get_charger_detail(request.get_json()['point_id'])

@app.route("/charger_detail/<point_id>")
def cg_detail(point_id):
    if session.get('logged_in'):    
        return render_template('charger_detail.html',point_id=point_id,api_user=api_user,api_key=api_key,username=session.get('username'),line_regis=get_line_auth(session.get('username')))
    return render_template('login.html')

@app.route("/dashboard")
def home():
    if session.get('logged_in'):
        return render_template('dashboard.html',api_user=api_user,api_key=api_key,username=session.get('username'),line_regis=get_line_auth(session.get('username')))
    return redirect('/')

@app.route('/api/test_get_device')
@auth.login_required
def got_device():
    return get_device()

@app.route('/api/update_api_path',methods=['POST'])
@auth.login_required
def got_path():
    return update_api_path(request.get_json()['device_name'],request.get_json()['api_path'])

@app.route('/api/get_charger')
@auth.login_required
def get_charger_point():
    return get_charger()

@app.route('/api/get_charger_config',methods=['POST'])
@auth.login_required
def got_charger_config():
    return get_charger_config(request.get_json()['point_id'])

@app.route('/api/get_user')
@auth.login_required
def got_user():
    return get_user()

@app.route('/api/get_log',methods=['POST'])
@auth.login_required
def got_log():
    return get_log(request.get_json()['point_id'])

@app.route('/api/approve',methods=['POST'])
def approved_user():
    return approve_user(request.form['user_id'])

@app.route('/api/update_status',methods=['POST'])
@auth.login_required
def update_status():
    return update_charger_point(request.get_json()['status'],request.get_json()['id'],request.get_json()['name'],request.get_json()['location'])
    # return update_charger_point(status,id,name,location)

@app.route('/api/get_line_auth')
@auth.login_required
def line_auth():
    return get_line_auth(session.get('username'))

@app.route('/api/update_line_auth/',methods=['POST'])
def update_line():
    update_line_register(request.form['username'])
    return redirect('/')

@app.route('/api/update_api/',methods=['POST'])
@auth.login_required
def updated_api():
    update_api(request.get_json()['point_id'],request.get_json()['api_path'])
    return redirect('/')

@app.route("/logout_access",methods = ['POST'])
def logout_access():
    session['logged_in'] = False
    if session.get('logged_in'):
        print("Still login")
    else:
        print("Log out")
    return redirect('/')


    
@app.route("/login_access",methods = ['POST'])
def login_access():
    go_login(request.form['username'],request.form['password'])

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))