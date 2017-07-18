# -*- coding: utf-8 -*-

# Send Decision: Server
import socket
import os
import sys

filepath="/home/pi/carpeta/Tesis/"
# We create a list with the address and the device; and the socket which it will listen
Connection = ("", 9022)

#We create a instantiation of the socket and we connect to it
server = socket.socket()

# We set the server to listen
try:
    server.bind(Connection)
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
# We accept a connection 
server.listen(1)
print "Listening to {0} in {1}".format(*Connection)
try:
    sck, addr = server.accept()
except socket.error as msg:
    sck.close()
    sys.exit()

print "Connected to: {0}:{1}".format(*addr)
#We open the file where we have saved the result of the process of decision making
with open(filepath + "pids/DecisionNode.txt", "r") as file: 
        decision=file.readline().rstrip()

try:
# We receive the message that the client is sending
    message = sck.recv(1024).strip()
    if message:
        print(message)
        #if we receive a message, we sent a message back with the result of the decision
        sck.send(decision)
        print(decision)
        with open(filepath + "pids/DecisionNetwork.txt", "w") as file1:
            print >> file1, message
except:
    print "Client (%s, %s) is offline" % addr
    sck.close()
    sys.exit()
    
#Everything is closed
server.close()
sck.close()
sys.exit()


