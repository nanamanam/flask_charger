#db.py
import os
import pymysql
from flask import jsonify,request,redirect,flash,session
import config as cfg
import json
import requests
import hashlib
from line_api import line_push
db_host=cfg.db['db_host']
db_user=cfg.db['db_user']
db_password=cfg.db['db_password']
db_name=cfg.db['db_name']
api_user=cfg.api['user']
api_key=cfg.api['key']
# db_user = os.environ.get('CLOUD_SQL_USERNAME')
# db_password = os.environ.get('CLOUD_SQL_PASSWORD')
# db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
# db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


def open_connection():
    # unix_socket = '/cloudsql/{}'.format(db_connection_name)
    unix_socket = '/cloudsql/noble-airport-391104:asia-southeast1:chargerdb'
    try:
        # if os.environ.get('GAE_ENV') == 'standard':
        conn = pymysql.connect(user=db_user, password=db_password,
                            # unix_socket=unix_socket,
                            host=db_host,port=3306,
                            db=db_name,
                            cursorclass=pymysql.cursors.DictCursor
                            )
    except pymysql.MySQLError as e:
        print(e)
    return conn

def update_device(data):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute("SELECT * FROM charger_point where name='"+str(data['name'])+"';")
        point = cursor.fetchall()
        list = []
        status=0
        alert=0
        if result > 0:
            if data['status']!=point[0]['status']:
                list.append("status="+str(data['status']))
                alert=1
                status=data['status']
            if data['plug1']!=point[0]['plug1']:
                list.append("plug1="+str(data['plug1']))
            if data['plug2']!=point[0]['plug2']:
                list.append("plug2="+str(data['plug2']))
            sql="UPDATE charger_point SET "
            c=0
            if len(list)>0:
                for i in list:
                    if c < len(list)-1:
                        sql+= i+","
                    else:
                        sql+= i
                    c=c+1
                sql+=" WHERE name='"+str(data['name'])+"';"
                # print(sql)
                result = cursor.execute(sql)
                conn.commit()
                if alert==1:
                    if status==1:
                        message={"group_id":0,"message": str(data['name'])+" is available !!"}
                    else:
                        message={"group_id":0,"message": str(data['name'])+" is down !!"}
                    print(message)
                    res=requests.post('https://charger-3a8c5.as.r.appspot.com/api/line_push', auth=(api_user,api_key),json=message)
                    print(res.status_code)
        else:
            got_point = 'NO POINT FOUND'
    conn.close()
      

def get_charger():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM charger_point;')
        point = cursor.fetchall()
        if result > 0:
            got_point = point
        else:
            got_point = 'NO POINT FOUND'
    conn.close()
    return got_point

def get_charger_config(point_id):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute("SELECT * FROM charger_config WHERE point_id='"+str(point_id)+"';")
        point = cursor.fetchall()
        if result > 0:
            got_point = point
        else:
            got_point = 'NO POINT FOUND'
    conn.close()
    return got_point

def get_charger_detail(point_id):
    conn = open_connection()
    with conn.cursor() as cursor:
        print("=====>",point_id)
        result = cursor.execute("SELECT * FROM charger_point WHERE point_id='"+str(point_id)+"';")
        point = cursor.fetchall()
        if result > 0:
            print(point)
            got_point = point
        else:
            got_point = 'NO POINT FOUND'
    conn.close()
    return got_point

def get_log(point_id):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute("SELECT * FROM error_log WHERE point_id='"+str(point_id)+"' order by id DESC;")
        log = cursor.fetchall()
        if result > 0:
            got_log = log
        else:
            got_log = {}
    conn.close()
    return got_log

def update_charger_point(status,id,name,location):
    conn = open_connection()
    with conn.cursor() as cursor:
        try:
            device="Device Alert\n"
            # flash('alert')
            # print("get",status,name,location)
            if status==0:
                device+= name+"("+location+") is down!"
                # flash(device)
                # print("status0 ",device)
            elif status==1:
                device+= name+"("+location+") is now online"
                # flash(device)
                # print("status1 ",device)
            
            result = cursor.execute("UPDATE charger_point SET status="+str(status)+" where point_id="+str(id)+";")
            group_id=0
            for i in get_line_group(group_id):
                if i['line_regis']==2:
                    # print(device)
                    line_push(i['line_id'],device)
            
        except Exception as e:
            print(e)
    conn.commit()
    conn.close()
    return redirect('/')

def add_user(username,password):
    conn = open_connection()
    with conn.cursor() as cursor:
        try:
            result = cursor.execute("INSERT INTO auth_user (username,password) VALUES ('"+str(username)+"','"+str(password)+"');")
        except Exception as e:
            print(e)
    conn.commit()
    conn.close()
    return

def update_line_auth(username,line_regis,line_id):
    conn = open_connection()
    with conn.cursor() as cursor:
        try:
            result = cursor.execute("UPDATE auth_user SET line_regis="+str(line_regis)+",line_id='"+str(line_id)+"' where username='"+str(username)+"';")
        except Exception as e:
            print(e)
    conn.commit()
    conn.close()
    return

def get_line_auth(username):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute("SELECT * FROM auth_user where username='"+str(username)+"';")
        point = cursor.fetchall()
        if result > 0:
            got_register = point
        else:
            got_register = 0
    conn.close()
    return got_register

def get_user():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute("SELECT id,username,status FROM auth_user;")
        point = cursor.fetchall()
        if result > 0:
            got_user = point
        else:
            got_user = 0
    conn.close()
    return got_user

def approve_user(id):
    conn = open_connection()
    with conn.cursor() as cursor:
        try:
            result = cursor.execute("UPDATE auth_user SET status=1 where id="+str(id)+";")
            conn.commit()
            conn.close()
            flash("user_id "+id+" has been approved")
        except Exception as e:
            print(e)
    return redirect('/')

def update_api(point_id,api_path):
    conn = open_connection()
    with conn.cursor() as cursor:
        try:
            result = cursor.execute("UPDATE charger_point SET api_path='"+str(api_path)+"' where point_id="+str(point_id)+";")
            conn.commit()
            conn.close()
            flash("updated API PATH")
        except Exception as e:
            print(e)
    return redirect('/')

def update_api_path(name,api_path):
    conn = open_connection()
    with conn.cursor() as cursor:
        try:
            result = cursor.execute("UPDATE charger_point SET api_path='"+str(api_path)+"' where name='"+str(name)+"';")
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
    return 'success'


def get_line_group(group_id):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute("SELECT * FROM auth_user where group_id='"+str(group_id)+"';")
        group_id = cursor.fetchall()        
    conn.close()
    return group_id

def check_line_auth(line_id):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute("SELECT * FROM auth_user where line_id='"+str(line_id)+"' limit 1;")
        point = cursor.fetchall()
        if result > 0:
            got_register = point[0]['line_regis']
        else:
            got_register = 0
    conn.close()
    return got_register

def update_line_register(username):
    conn = open_connection()
    with conn.cursor() as cursor:
        try:
            result = cursor.execute("SELECT line_id FROM auth_user where username='"+str(username)+"';")
            point = cursor.fetchall()
            line_id=point[0]['line_id']
            result = cursor.execute("UPDATE auth_user SET line_regis='2' where username='"+str(username)+"';")
            flash("line user:"+username+" has been enabled")
            line_push(line_id,'คุณได้ยืนยันตัวตนเรียบร้อย คุณจะสามารถได้รับข้อความแจ้งเตือนจากระบบ')
        except Exception as e:
            print(e)
    conn.commit()
    conn.close()
    return  

def add(song):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO charger_point (name, location) VALUES(%s, %s)', (song["name"], song["location"]))
    conn.commit()
    conn.close()

def check_basic_auth(username,password):
    if username==api_user and password==api_key:
        return True


    return False

def go_login(username,password):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * from auth_user where username='"+username+"'")
        if len(cursor.fetchall())>0:
            cursor.execute("SELECT * from auth_user where username='"+username+"'")
            # print("len",len(cursor.fetchall()))
            for row in cursor:
                if row['status']==1:
                    password_key=hashlib.sha224(password.encode('utf-8')).hexdigest()
                    if row['lock_status']!=1:
                        if row['password']==password_key:
                            session['logged_in'] = True
                            session['user_id'] = row['id']
                            session['username'] = row['username']
                            cursor.execute("UPDATE auth_user SET attemp=0 where id="+str(row['id'])+"")
                            conn.commit()
                            conn.close()
                            return redirect('/')
                            # return True
                        else:
                            attemp=row['attemp']+1
                            remain=3-attemp
                            lock=0
                            if attemp==3:
                                lock=1
                            flash("Password incorrect : Remain "+str(remain)+" attemp and will lock forever!")
                            sql_query="UPDATE auth_user SET attemp="+str(attemp)+",lock_status="+str(lock)+" where id="+str(row['id'])
                            cursor.execute(sql_query)
                            conn.commit()
                            conn.close()
                            return redirect('/')
                    else:
                        flash("This account has been locked forever!!")
                        return redirect('/')
                else:
                    flash("Waiting for approved")

        else:
            cursor.close()
            flash("Username not found")