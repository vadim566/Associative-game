import random
import threading
import time
import json
from concurrent.futures import ThreadPoolExecutor
from os.path import isdir, isfile, join

from flask_cors import CORS

import requests
from flask import Flask, url_for, redirect, request, send_from_directory, jsonify
from leader_election import LeaderElection
import TF_IDF
import os




# returning a list with files in dir_path
def filesinDir(dir_path):
    try:
        files_in_dir = [f for f in os.listdir(dir_path) if isfile(join(dir_path, f))]
    except:
        "something wrong with the directory, put in the full path"
    finally:
        return files_in_dir


# returning a list with sub dir to dir_path
def dirinDir(dir_path):
    try:
        dir_in_dir = [f for f in os.listdir(dir_path) if isdir(join(dir_path, f))]
    except:
        "something wrong with the directory, put in the full path"
    finally:
        return dir_in_dir



app = Flask(__name__)
CORS(app, support_credentials=True)
lock=threading.RLock()
#answer = LeaderElection('localhost:2181', 'Term', '/TF-IDF')

le = LeaderElection('localhost:2181', 'Leader', '/election')
le.register()

#tfIDF
bookLib = ".\\books\\"
sub_folder = dirinDir(bookLib)

# files = TF_IDF.filesinDir(".\\books\\")
#query = 'bell'
#test_query = []

test_dics = []

# leader


hostname=""


def str_tuple_decode_to_tuple(tuple_str :bytes)->tuple:
    decode=tuple_str.decode()
    tup_data=decode[1:-1].split(",")
    ip=tup_data[0].split("'")[1]
    type=tup_data[1].split("'")[1]
    return ip,type

def get_service_host(master :LeaderElection):
    connection_data = le.get_children_data("/services")
    children_host=[]
    for cd in connection_data:
        child=str_tuple_decode_to_tuple(cd)
        if child[1]=="worker":
            children_host.append(child)
    return children_host


def make_request_to_worker(children_host :list,query:str,sub_folder:int):
    #lock.acquire()
    #test_dics=[]
    ch=children_host

    msg = json.loads(requests.request(method='get', url="http://" + ch + ":5000/"+query+"/"+str(sub_folder)).text)
    global lock
    lock.acquire()
    test_dics.append(msg)
    lock.release()




@app.route("/" ,methods=['get','post'])
def get_random_phrase():
    words = []
    while len(words) < 12  :
        num_folder=random.randint(0,len(sub_folder)-1)
        fldr = bookLib + sub_folder[num_folder]
        num_files_in_dir=len(filesinDir(fldr))
        num_story=random.randint(0,num_files_in_dir-1)
        name_of_story=filesinDir(fldr)[num_story]
        read_file = open(fldr+'\\' + name_of_story, 'r')

        Lines = read_file.readlines()
        num_of_line=random.randint(0,len(Lines))
        line_txt=Lines[num_of_line]
        line_len=len(line_txt)
        words = line_txt.split()
    read_file.close()
    num_of_words=len(words)
    rnd_num=random.randint(0, num_of_words-5)
    words_to_front=[words[rnd_num],words[rnd_num+1],words[rnd_num+2],words[rnd_num+3],words[rnd_num+4]]

    return jsonify(" ".join(words_to_front))








@app.route("/<query>", methods=['get', 'post'])

def main(query):
    if le.is_leader():
        global test_dics
        test_dics=[]
        msg=[]
        children_host=le.sd.workers_ip
        pool = ThreadPoolExecutor(max_workers=len(children_host)+1)
        #i=0
       # for ch in children_host:
       #    msg=json.loads(requests.request(method='get', url="http://" + ch[0]+":5000/").text)
       #     test_dics.append(msg
        #    i += 1
        leader_test = TF_IDF.TF_IDF(bookLib=bookLib, files=TF_IDF.filesinDir(str(bookLib)), query=query)

        threads=[]
        for i in range(len(sub_folder)):
         worker_thread=threading.Thread(target=make_request_to_worker,args=(children_host[i%len(children_host)],query,i))
         worker_thread.start()
         threads.append(worker_thread)
        for w in threads:
            w.join()

        #test_dics.append(test_query[i].TF_dic)
        leader_test.leader(test_dics)
        leader_test.score_items_LEADER()
        leader_test.pracentage_score()
        leader_test.sort_values()
        msg=leader_test.sorted_terms_score
        json_msg=json.dumps(dict(msg))
        leader_test.TF_dic = {}
        return app.make_response(json_msg)
        #return  json_msg


@app.route('/favicon.ico', methods=['get','post'])
@app.route('/<query>/favicon.ico', methods=['get','post'])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico.png', mimetype='image/vnd.microsoft.icon')


@app.route("/<query>/<subfolder>", methods=['get', 'post'])
def worker_TF(query,subfolder):
    if not le.is_leader() :
        body=worker_request(query,int(subfolder))
        return body



def worker_request(query : str,subfolder :int):
    test_query = []
   # test_dics = []
    i = subfolder
    test_query.append(TF_IDF.TF_IDF(bookLib=str(bookLib) + str(sub_folder[i]),
                                    files=TF_IDF.filesinDir(str(bookLib) + str(sub_folder[i])+'\\'), query=query))
    test_query[0].worker()
    json_msg = json.dumps(test_query[0].TF_dic)
    return json_msg
    #return term + str("my ip is:" + le.get_service()[0] + " and my role is:" + le.get_service()[1])






def ping_host(hostname,ip_range=1):
    for i in range(ip_range):
        hostname=hostname[:-1]+str(i+2)
        response = os.system("ping -n 1 " + hostname)
        if response==1:#
            return i+2
    return ip_range

if __name__=="__main__":
    children=le.get_children()
    num_of_children=len(children)
    ip_sufix=ping_host("127.0.0.1",num_of_children)
    hostname="127.0.0."+str(ip_sufix)
    if le.is_leader():
        le.service_register(ip=hostname,service="master")
    if not le.is_leader():
        le.service_register(ip=hostname,service="worker")
    app.run(host=hostname)





    #and then check the response...
