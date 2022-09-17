import kazoo.client
from flask import Flask, url_for, redirect,request
from leader_election import LeaderElection
from kazoo.client import KazooClient, KazooState
from kazoo.protocol.states import EventType, WatchedEvent
import os
import pyping2


app = Flask(__name__)



le = LeaderElection('localhost:2181', 'Game', '/election')
le.register()


if le.is_leader():
    @app.route("/")
    @app.route("/<term>")
    def main(phrase="david"):
        # if leader
        msg = ('I am Leader\n')
        return msg

else:
    @app.route("/")
    @app.route("/<term>")
    def worker(term=""):

            msg = ('I am Worker\n')
            return msg




def ping_host(hostname,ip_range=1):
    for i in range(ip_range):
        hostname=hostname[:-1]+str(i+2)
        response = os.system("ping -n 1 " + hostname)
        if response==1:#
            return i+2
    return ip_range

if __name__=="__main__":
    if le.is_leader():
        app.run()
    else:
        children=le.get_children()
        num_of_children=len(children)
        ip_sufix=ping_host("127.0.0.1",num_of_children)
        app.run(host="127.0.0."+str(ip_sufix))



    #and then check the response...
