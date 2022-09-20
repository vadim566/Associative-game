import random
import time

import kazoo.client
import requests
from flask import Flask, url_for, redirect,request
from leader_election import LeaderElection
from kazoo.client import KazooClient, KazooState
from kazoo.protocol.states import EventType, WatchedEvent
import os
import pyping2


app = Flask(__name__)


#answer = LeaderElection('localhost:2181', 'Term', '/TF-IDF')

le = LeaderElection('localhost:2181', 'Leader', '/election')
le.register()
if le.is_leader():
    answer = LeaderElection('localhost:2181', 'Answer', '/answer')
    answer.register()

hostname=""



def work_to_do(phrase,ip_sufix):
    x=int(hostname[-1])
    x=str(x+ip_sufix+1)
    address = hostname[:-1]+str(x)+":5000"+"/"+phrase

    x=requests.request(method='get',url="http://"+address)

    return x.text


if le.is_leader():
    @app.route("/" ,methods=['get','post'])
    @app.route("/<term>", methods=['get', 'post'])

    def main(term="test"):

            # if leader
            #msg=[]
            #msg.append('I am Leader\n')
           # for i in range(2):
            #    msg.append(work_to_do(term,i))
            #return msg

            le.set_children_data(term)
            time.sleep(5)
            values=answer.get_children_data()
            values=set(values)
            le.set_children_data("")
            answer.clean_zookeeper("/answer")
            return str(values)
     #   else:
      #  return "i am worker waiting for work"



if not le.is_leader():
    le.set_data_self("")
    while True:
        time.sleep(2)
        if not le.get_data_self()[0]==b"":
                msg=le.get_data_self()[0]
                x=random.randint(1,6)
                term=str(msg)+str(x)
               # le.set_data_self(term)
                answer = LeaderElection('localhost:2181', 'answer', '/answer')
                answer.register()
                answer.set_data_self(term)
                le.set_data_self("")
              #  answer = LeaderElection('localhost:2181', 'term', '/TF-IDF')
              #   answer.register()




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

   # else:
    #    children=le.get_children()
     #   num_of_children=len(children)
      #  ip_sufix=ping_host("127.0.0.1",num_of_children)
       # hostname="127.0.0."+str(ip_sufix)
        #app.run(host=hostname)




    #and then check the response...
