from flask import Flask, render_template, make_response,request,redirect,url_for, session
from turbo_flask import Turbo
import random
import threading
import time


app = Flask(__name__, static_url_path='/static')
app.secret_key = '123456'
turbo = Turbo(app)
PNI = "ON"
global numeroS
numeroS = 0
global numeroD
numeroD = 0
global Fcmin
Fcmin = 60
global Fcmax
Fcmax = 100
global Satmin
Satmin = 90
global Satmax
Satmax = 100

def update_load():
    with app.app_context():
        while True:
            time.sleep(2)
            turbo.push(turbo.replace(render_template('pni.html'), 'loadB'))
            turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))

#def pni():
  #  global numeroS
   # global numeroD
    #if numeroS and numeroD != 0:
     #   if pressed button:
      #      display PNI

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.context_processor
def inject_load():
    global numeroS
    global numeroD
    global Fcmin
    global Fcmax
    global Satmin
    global Satmax
    load = [int(random.randint(int(Fcmin), int(Fcmax))), int(random.randint(int(Satmin), int(Satmax)))]
    PAS = numeroS
    PAD = numeroD
    return {'FC': load[0], 'SAT': load[1], 'PAS': PAS, 'PAD': PAD}

@app.route('/homepage')
def home_page():
    return render_template("homepage.html")

@app.route('/fetch_dataPNI', methods=['POST','GET'])
def FetchDataPNI():
    global numeroS
    global numeroD
    if request.method == "POST":
        numeroS = request.form['numberS']
        numeroD = request.form['numberD']
        return render_template('control.html')

@app.route('/fetch_dataFC', methods=['POST','GET'])
def FetchDataFC():
    global Fcmin
    global Fcmax
    if request.method == "POST":
        Fcmin = request.form['FCmin']
        Fcmax = request.form['FCmax']
        return render_template('control.html')

@app.route('/fetch_dataSat', methods=['POST','GET'])
def FetchDataSat():
    global Satmin
    global Satmax
    if request.method == "POST":
        Satmin = request.form['Satmin']
        Satmax = request.form['Satmax']
        return render_template('control.html')

@app.route('/control' , methods=['POST','GET'])
def control():
    return render_template("control.html")

if __name__ == "__main__":
    app.run(debug = True)