import signal
from leader_election import LeaderElection
import time

def handler(signum, frame):
    print("Ctrl-c was pressed.\nEXIT", end="", flush=True)
    exit(1)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)

    le = LeaderElection('localhost:2181', 'cmdApp', '/election')
    le.register()

    # let's make ourselves busy with some tasks
    counter = 0
    while True:
        if le.is_leader():
            #if leader
            msg = ('I am Leader\n')
            print(msg.upper())
            time.sleep(1)
        else:
            #if worker
            msg =('I am Worker - give me some text\n')
            print(msg.upper())
            #make some calculations
            counter += 1
            print('calc...' + str(counter))
            time.sleep(1)


