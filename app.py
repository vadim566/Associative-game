import random
import time
import json
import requests
from flask import Flask, url_for, redirect,request
from leader_election import LeaderElection
import TF_IDF
import os



app = Flask(__name__)


#answer = LeaderElection('localhost:2181', 'Term', '/TF-IDF')

le = LeaderElection('localhost:2181', 'Leader', '/election')
le.register()

#tfIDF
sub_folder = ['a\\', 'b\\', 'c\\']
bookLib = ".\\books\\"
# files = TF_IDF.filesinDir(".\\books\\")
query = 'bell'
test_query = []

test_dics = []

# leader
leader_test = TF_IDF.TF_IDF(bookLib=bookLib, files=TF_IDF.filesinDir(str(bookLib)), query=query)

hostname=""



def work_to_do(phrase,ip_sufix):
    x=int(hostname[-1])
    x=str(x+ip_sufix+1)
    address = hostname[:-1]+str(x)+":5000"+"/"+phrase

    x=requests.request(method='get',url="http://"+address)

    return x.text

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

@app.route("/" ,methods=['get','post'])
@app.route("/<term>", methods=['get', 'post'])

def main(term="test"):
    if le.is_leader():
        msg=[]
        children_host=get_service_host(le)
        for ch in children_host:
            msg=json.loads(requests.request(method='get', url="http://" + ch[0]+":5000/").text)
            test_dics.append(msg)
        #test_dics.append(test_query[i].TF_dic)
        leader_test.leader(test_dics[0])
        leader_test.score_items_LEADER()
        leader_test.pracentage_score()
        leader_test.sort_values()
        msg=leader_test.sorted_terms_score
        return str(msg)
    else:
        i=0
        test_query.append(TF_IDF.TF_IDF(bookLib=str(bookLib) + str(sub_folder[i]),
                                        files=TF_IDF.filesinDir(str(bookLib) + str(sub_folder[i])), query=query))
        test_query[i].worker()
        json_msg=json.dumps(test_query[i].TF_dic)
        return json_msg





        return term+str("my ip is:"+le.get_service()[0]+" and my role is:"+le.get_service()[1])






def ping_host(hostname,ip_range=1):
    for i in range(ip_range):
        hostname=hostname[:-1]+str(i+2)
        response = os.system("ping -n 1 " + hostname)
        if response==1:#
            return i+2
    return ip_range

if __name__=="__main__":



    while not le.is_leader():
        children=le.get_children()
        num_of_children=len(children)
        ip_sufix=ping_host("127.0.0.1",num_of_children)
        hostname="127.0.0."+str(ip_sufix)
        le.service_register(ip=hostname)
        app.run(host=hostname)

    time.sleep(5)

    while le.is_leader():
        hostname = "127.0.0.1"
        le.service_register("master")
        app.run(host=hostname)



    #and then check the response...
