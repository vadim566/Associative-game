# This is a sample Python script.

import threading
import socket


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



#WEB SERVER
SERVER_IP='localhost'
SERVER_PORT=5000
BUFFERSIZE=4*1024
HTTP_HEAD='HTTP /1.0 200 OK\n\n'
def client_respond(cSoc,cAdd):
    with cSoc as soc:
            data=soc.recv(BUFFERSIZE)
            if not data:
                print(f"connection close with {cAdd}")
                return
            else:
                route=data.decode().splitlines()[0].split(' ')[1]
                if route=='/hello':#hello route
                    body="<HTML><body><h1>u got the hello page</h1></body></HTML>"
                elif  route =='/home':#home route
                    body="<HTML><body><h1>u got the home page</h1></body></HTML>"
                else:#another routes
                        body = "<HTML><body><h1>There is no such page, try hello or home</h1></body></HTML>"
                response=HTTP_HEAD+body
                soc.sendall(response.encode())





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with  socket.socket(socket.AF_INET,socket.SOCK_STREAM) as socket:
        socket.bind((SERVER_IP,SERVER_PORT))
        print(f"ip and port bounded\n The Server runs on {SERVER_IP} : {SERVER_PORT}")
        socket.listen()
        while True:
            cSoc, cAdd=socket.accept()
            threading.Thread(target=client_respond,args=(cSoc,cAdd)).start()
        print(f"The server closed successfully")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
