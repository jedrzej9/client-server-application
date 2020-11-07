import socket
import sys
import pickle
import json
from thread import *


def writeToJSON(path, fileName, data):
    filePathName = './' + path + fileName + '.json'
    with open(filePathName, 'w') as fp:
        json.dump(data, fp)


HOST = '127.0.0.1'  # Symbolic name meaning all available interfaces
PORT = 8888  # Arbitrary non-privileged port
TASKS = []

# Save to JSON file
path = './'
fileName = 'ToDoList'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

# Start listening on socket
s.listen(10)
print 'Socket now listening'


# Function for handling connections. This will be used to create threads
def clientthread(conn):
    # infinite loop so that function do not terminate and thread do not end.
    while True:
        # Receiving from client

        data = pickle.loads(conn.recv(4096))
        print(data)
        if data[0] == 'h':
            message = pickle.dumps(TASKS)
            conn.sendall(message)

        if data[0] == 'j':
            TASKS.append(data[-2:])
            reply = 'Zadanie o tresci: ' + data[1] + ' z priorytetem: ' + data[2] + ' zostalo dodane do listy'
            conn.sendall(reply)
            writeToJSON(path, fileName, TASKS)

        if data[0] == 'k':
            tmp = int(data[1])
            TASKS.pop(tmp - 1)
            reply = 'Zadanie o ID: ' + data[1] +  ' zostalo usuniete z listy'
            conn.sendall(reply)
            writeToJSON(path, fileName, TASKS)

        if data[0] == 'l':
            tmp = int(data[1])
            message = []
            for i in TASKS:
                if int(i[1]) == tmp:
                    message.append(i)
            reply = pickle.dumps(message)
            conn.sendall(reply)

        if not data:
            break

        # reply = 'Wyswietlam zadania  ' + data
        # conn.sendall(reply)

    # came out of loop
    conn.close()


# now keep talking with the client
while 1:
    # wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function
    start_new_thread(clientthread, (conn,))

s.close()