from flask import Flask, url_for, redirect, request, send_from_directory, render_template,jsonify
import json
from flask_cors import CORS

import os

app = Flask(__name__)
CORS(app, support_credentials=True)
@app.route('/favicon.ico', methods=['get','post'])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico.png', mimetype='image/vnd.microsoft.icon')



@app.route('/' ,methods=['get', 'post'])
def home():
    return render_template('index.html')




if __name__=="__main__":
    hostname='127.0.0.10'
    app.run(host=hostname)