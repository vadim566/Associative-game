import sys
import time

from kazoo.client import KazooClient, KazooState
from kazoo.protocol.states import EventType, WatchedEvent

ZNODE_PREFIX = '/a_'

class LeaderElection():
    def __init__(self, zooKeeperAddresses, nodeName, electionNamespace):
        self.zooKeeperAddresses = zooKeeperAddresses
        self.nodeName: str = nodeName
        self.electionNamespace = electionNamespace
        self.zk: KazooClient = None
        self._connect_zookeeper()
        self._leader = False


    @staticmethod
    def connection_status_listener(state):
        if state == KazooState.LOST:
            print('session to zookeeper was lost')  # Register somewhere that the session was lost
        elif state == KazooState.SUSPENDED:
            print('disconnected from zookeeper')  # Handle being disconnected from Zookeeper
        else:
            print('connected to zookeeper')  # Handle being connected/reconnected to Zookeeper

    def _connect_zookeeper(self):
        self.zk = KazooClient(hosts=self.zooKeeperAddresses)
        self.zk.start()
        self.zk.add_listener(self.connection_status_listener)  # notify about connection change


    def register(self):
        path = self.electionNamespace + ZNODE_PREFIX

        #create ephemeral Znode to represent the node (will create electionNamespace if not exists)
        new_node_path = self.zk.create(path=path, value=self.nodeName.encode(), ephemeral=True, sequence=True, makepath=True)
        self.znode_name = new_node_path.split('/')[-1]

        self.elect_leader()


    def elect_leader(self):
        print('leader_election: start')
        children = self.zk.get_children(path=self.electionNamespace)
        sorted_children = sorted(children)
        if sorted_children[0] == self.znode_name:
            self._leader = True
            print("LEADER: " + self.nodeName + '(znode: ' + self.znode_name + ')')
        else:
            print("Follower: " + '(znode: ' + self.znode_name + ')')
            predecessor_index = sorted_children.index(self.znode_name) -1
            print('Watching znode: ' + str(sorted_children[predecessor_index]))
            @self.zk.DataWatch(self.electionNamespace + '/' + sorted_children[predecessor_index])
            def register_next(data, stat, event):
                #race condition: it could be that the DataWatch failed as the predecessor node died during the time
                # between the get_children() and the DataWatch registration
                #to identify a failed watch registration: check that all the function params are None
                if data is None and stat is None:
                    #watch registration failed
                    self.elect_leader()
                    return
                if event is not None:
                    if event.type == EventType.DELETED:
                        print("Event is " + str(event))
                        self.elect_leader()

    def clean_zookeeper(self,path=""):
        if(path==""):
            path=self.electionNamespace

        self.zk.delete(path, recursive=True)

    def is_leader(self) -> bool:
        return self._leader

    def get_children(self):
        children = self.zk.get_children(path=self.electionNamespace)
        return children

    def __repr__(self):
        return 'Leader ' if self._leader is True else '' + self.nodeName + '(' + self.znode_name + ')'

    def set_children_data(self,term):
        children=self.zk.get_children(path=self.electionNamespace)
        for child in children:
            self.zk.set(path=self.electionNamespace+"/"+child,value=term.encode('utf-8'))


    def get_children_data(self,path=""):
        if path=="":
            path= self.electionNamespace
        values=[]
        children = self.zk.get_children(path=path)
        for child in children:
            values.append(self.zk.get(path=path + "/" + child)[0])
        return values
    def set_data_self(self,term):
        self.zk.set(path=self.electionNamespace+"/"+self.znode_name,value=term.encode('utf-8'))
    def get_data_self(self):
        value=self.zk.get(path=self.electionNamespace+"/"+self.znode_name)
        return  value



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('use leader_election.py <appName>')
        exit(-1)
    appName = sys.argv[1]
    leaderElection: LeaderElection = LeaderElection('localhost:2181', appName, '/election')
    #leaderElection.clean_zookeeper()

    leaderElection.register()

    try:
        time.sleep(300)
    finally:
        print('\n node interrupted')
        leaderElection.zk.stop()
        leaderElection.zk.close()
        print('\n node is dead')



