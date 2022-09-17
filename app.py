import kazoo.client
import requests
from flask import Flask, url_for, redirect,request
from leader_election import LeaderElection
from kazoo.client import KazooClient, KazooState
from kazoo.protocol.states import EventType, WatchedEvent
import os
import pyping2


app = Flask(__name__)



le = LeaderElection('localhost:2181', 'Game', '/election')
le.register()
hostname=""



def work_to_do(phrase,ip_sufix):
    x=int(hostname[-1])
    x=str(x+ip_sufix+1)
    address = hostname[:-1]+str(x)+":5000"+"/"+phrase

    x=requests.request(method='get',url="http://"+address)

    return x.text



@app.route("/" ,methods=['get','post'])


def main(term="david"):
    if le.is_leader():
        # if leader
        msg=[]
        msg.append('I am Leader\n')
        for i in range(2):
            msg.append(work_to_do(term,i))
        return msg
    else:
        return "i am worker waiting for work"

@app.route("/<term>", methods=['get', 'post'])
def worker(term=""):
    if not le.is_leader():
        msg = ('I am Worker'+term+'\n')
        return msg
    else:
        redirect("/")




def ping_host(hostname,ip_range=1):
    for i in range(ip_range):
        hostname=hostname[:-1]+str(i+2)
        response = os.system("ping -n 1 " + hostname)
        if response==1:#
            return i+2
    return ip_range

if __name__=="__main__":
    if le.is_leader():
        hostname = "127.0.0.1"
        app.run()

    else:
        children=le.get_children()
        num_of_children=len(children)
        ip_sufix=ping_host("127.0.0.1",num_of_children)
        hostname="127.0.0."+str(ip_sufix)
        app.run(host=hostname)




    #and then check the response...
