import os
import random
from flask import Flask
from flask_httpauth import HTTPBasicAuth
app = Flask(__name__)
auth = HTTPBasicAuth()
@app.route('/api')
@auth.login_required
def fetch_api():
    data = {"name":"device1",
            "status": 1,
            "plug1":random.randrange(0,400),
            "plug2":random.randrange(0,400)
    }
    return data

@auth.verify_password
def authenticate(username, password):
    if username=='charger_api' and password=='12312312388':
            return True
    return False


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
