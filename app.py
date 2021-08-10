from flask import Flask, render_template, make_response,request,redirect,url_for, session
from turbo_flask import Turbo
import random
import re
import sys
import threading
import time


app = Flask(__name__, static_url_path='/static')
app.secret_key = '123456'
turbo = Turbo(app)
PNI = "ON"
def update_load():
    with app.app_context():
        while True:
            time.sleep(2)
            turbo.push(turbo.replace(render_template('pni.html'), 'loadB'))
            turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))

def pni():
    PA =[120, 90]
    return 120

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.context_processor
def inject_load():
    load = [int(random.randint(70, 100)), int(random.randint(89, 99))]
    PAS = "120"
    PAD = "90"
    return {'FC': load[0], 'SAT': load[1], 'PAS': PAS, 'PAD': PAD}

@app.route('/homepage')
def home_page():
    return render_template("homepage.html")

@app.route('/fetch_data', methods=['POST','GET'])
def FetchData():
    if request.method == "POST":
        numeroS = request.form['numberS']
        session["numeroS"] = numeroS
        numeroD = request.form['numberD']
        session["numeroD"] = numeroD
        return render_template('control.html')

@app.route('/control' , methods=['POST','GET'])
def control():
    return render_template("control.html")

if __name__ == "__main__":
    app.run(debug = True)