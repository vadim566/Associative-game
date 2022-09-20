import threading
from kazoo.client import KazooClient,KazooState
import socket
import  requests
def connection_status_listener(state):
    if state == KazooState.LOST:
        print('session to zookeeper was lost')
    elif state == KazooState.SUSPENDED:
        print('disconnected from zookeeper')
    else:
        print('connected to zookeeper')



class ServiceDiscovery():
    my_lock=threading.RLock

    def __init__(self, zk:KazooClient):
        self.zk: KazooClient =zk
        self.services=None
        self.SERVICE_REGISTRY_NAMESPACE='/services'
        self.ZNODE_PREFIX='s_'

    def register(self,service:str):
        hostname=socket.gethostname()
        my_ip : str =socket.gethostname('localhost')
        data_tup=(my_ip,service)
        new_node_path=self.zk.create(
            path=self.SERVICE_REGISTRY_NAMESPACE+'/'+self.ZNODE_PREFIX,
            value=data_tup.__repr__().encode(),
            ephemeral=True,
            sequence=True,
            makepath=True
        )
        print('register '+ str(new_node_path))

    def close(self):
        self.zk.stop()
        self.zk.close()

    def get_services(self):
        self.my_lock.acquire()
        body_data=requests.request(method='get',url='http://'+self.services[0]+":5000")
        self.my_lock.release()
        return body_data

