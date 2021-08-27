# Programado en Agosto/2021 por Pablo Arroyo Z.

from flask import Flask, render_template, request
from turbo_flask import Turbo
import random
import threading
import time

app = Flask(__name__, static_url_path='/static')
app.secret_key = '123456'
turbo = Turbo(app)

numeroS = 1
numeroD = 1
Fcmin = 60
Fcmax = 100
Satmin = 90
Satmax = 100
PNI = 0


def update_load():
    with app.app_context():
        global PNI
        print(PNI)
        while True:
            time.sleep(2)
            turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))
            #print(PNI)
            #print(numeroS)
            #print(numeroD)
            if PNI == 1:
                PNI = 0
                turbo.push(turbo.replace(render_template('pni.html'), 'loadB'))


@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.context_processor
def inject_load():
    global numeroS
    nS = int(numeroS)
    global numeroD
    nD = int(numeroD)
    global Fcmin
    global Fcmax
    global Satmin
    global Satmax
    global PNI
    load = [int(random.randint(int(Fcmin), int(Fcmax))), int(random.randint(int(Satmin), int(Satmax)))]
    loadB = [nS, nD]
    return {'FC': load[0], 'SAT': load[1], 'PAS': loadB[0], 'PAD': loadB[1]}


@app.route('/fetch_button_pni', methods=['POST', 'GET'])
def fetch_button_pni():
    global PNI
    if "PNI" in request.form:
        PNI = 1
    else:
        PNI = 0
    return render_template('index.html')


@app.route('/fetch_dataPNI', methods=['POST', 'GET'])
def fetch_data_pni():
    global numeroS
    global numeroD
    if request.method == "POST":
        numeroS = request.form['numberS']
        numeroD = request.form['numberD']
        return render_template('control.html')


@app.route('/fetch_dataFC', methods=['POST', 'GET'])
def fetch_data_fc():
    global Fcmin
    global Fcmax
    if request.method == "POST":
        Fcmin = request.form['FCmin']
        Fcmax = request.form['FCmax']
        return render_template('control.html')


@app.route('/fetch_dataSat', methods=['POST', 'GET'])
def fetch_data_sat():
    global Satmin
    global Satmax
    if request.method == "POST":
        Satmin = request.form['Satmin']
        Satmax = request.form['Satmax']
        return render_template('control.html')


@app.route('/control', methods=['POST', 'GET'])
def control():
    return render_template("control.html")


if __name__ == "__main__":
    app.run(debug=True)
