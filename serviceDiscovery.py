import threading
from kazoo.client import KazooClient,KazooState
import socket
import  requests
from stringToTuple import str_tuple_decode_to_tuple
def connection_status_listener(state):
    if state == KazooState.LOST:
        print('session to zookeeper was lost')
    elif state == KazooState.SUSPENDED:
        print('disconnected from zookeeper')
    else:
        print('connected to zookeeper')



class ServiceDiscovery():
    my_lock=threading.RLock()

    def __init__(self, zk:KazooClient):
        self.zk: KazooClient =zk
        self.services=None
        self.SERVICE_REGISTRY_NAMESPACE='/services'
        self.ZNODE_PREFIX='s_'
        self.workers=None
        self.workers_ip=[]
    def register(self,service:str,ip):
        hostname=socket.gethostname()
        if ip=="":
            my_ip : str =socket.gethostbyname('localhost')
        else:
            my_ip=ip
        data_tup=(my_ip,service)
        new_node_path=self.zk.create(
            path=self.SERVICE_REGISTRY_NAMESPACE+'/'+self.ZNODE_PREFIX,
            value=data_tup.__repr__().encode(),
            ephemeral=True,
            sequence=True,
            makepath=True
        )

        self.services=data_tup
        print('register '+ str(new_node_path))


    def close(self):
        self.zk.stop()
        self.zk.close()


    def get_services(self):
        ip=self.services[0]
        service=self.services[1]
        return ip,service

    def get_worker_discover(self):
        self.my_lock.acquire()
        if self.workers == None:
            @self.zk.ChildrenWatch(self.SERVICE_REGISTRY_NAMESPACE)
            def update_list(children):
                self.workers = []
                self.workers_ip=[]
                for child in children:
                  str_tuple_child=self.zk.get(path=self.SERVICE_REGISTRY_NAMESPACE+'/'+child)[0]
                  tuple_child=str_tuple_decode_to_tuple(str_tuple_child)
                  if tuple_child[1]=='worker':
                    self.workers_ip.append(tuple_child[0])
                    self.workers.append(tuple_child)



