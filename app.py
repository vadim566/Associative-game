import random
import time

import requests
from flask import Flask, url_for, redirect,request
from leader_election import LeaderElection

import os



app = Flask(__name__)


#answer = LeaderElection('localhost:2181', 'Term', '/TF-IDF')

le = LeaderElection('localhost:2181', 'Leader', '/election')
le.register()



hostname=""



def work_to_do(phrase,ip_sufix):
    x=int(hostname[-1])
    x=str(x+ip_sufix+1)
    address = hostname[:-1]+str(x)+":5000"+"/"+phrase

    x=requests.request(method='get',url="http://"+address)

    return x.text



@app.route("/" ,methods=['get','post'])
@app.route("/<term>", methods=['get', 'post'])

def main(term="test"):
    if le.is_leader():
        connection_data=le.get_children_data("/services")
        return str(connection_data)
    else:
        return term+str(le.get_service())






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

    while le.is_leader():
        hostname = "127.0.0.1"
        le.service_register("master")
        app.run(host=hostname)



    #and then check the response...
