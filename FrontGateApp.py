from flask import Flask, url_for, redirect, request, send_from_directory, render_template,jsonify
import json
from flask_cors import CORS
from leader_election import LeaderElection

import os

le = LeaderElection('localhost:2181', 'FrontEnd', '/Front')
le.register()


app = Flask(__name__)
CORS(app, support_credentials=True)

def get_master():
    le.zk.get('/services/' + sorted(le.zk.get_children('/services/'))[0])[0]
    b"('127.0.0.2', 'master')"
    main_server = le.zk.get('/services/' + sorted(le.zk.get_children('/services/'))[0])[0]
    server_ip = le.str_tuple_decode_to_tuple(main_server)[0]
    return server_ip

@app.route('/get_master_req',methods=['get','post'])
def get_master_req():
    server_ip=get_master()
    return jsonify(server_ip)

@app.route('/favicon.ico', methods=['get','post'])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico.png', mimetype='image/vnd.microsoft.icon')



@app.route('/' ,methods=['get', 'post'])
def home():
    master_ip=get_master()
    return render_template('index.html',main_server=master_ip)




if __name__=="__main__":
    hostname='127.0.0.10'
    app.run(host=hostname)