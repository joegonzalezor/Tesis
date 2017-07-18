# -*- coding: utf-8 -*-
 
# Send Decision: Client 
import socket
import sys
import os 
# We create a list with the address of the server and the number of the socket
Connection = ("10.42.0.21", 9022)
filepath = "/home/pi/carpeta/Tesis/" 
# We create a instantiation of the socket and we connect to it
try:
    client = socket.socket()
except socket.error:
    print 'Failed to create socket'
    sys.exit(0)
try:
    client.connect(Connection)
except socket.error as msg:
    client.close()
    print("error")
    #A value is send if there is a error
    sys.exit(0)
    #We open the file where we have saved the result of the process of decision making
with open(filepath + "pids/DecisionNode.txt", "r") as File:
    decision=File.readline().rstrip()
try:
    #We Send the decision information
    print ("Sending decision information")
    client.send(decision)
    #We recieve the decision from the Server   
    message=client.recv(1024).strip()   
    print("Message received :" + message)    
    with open(filepath + "pids/DecisionNetwork.txt", "w") as file1:
        print >> file1, message   

except socket.error:
    #Send failed
    print 'Send failed'
    client.close()
    sys.exit(0)
print("Ok")
#If there is a error, we sent a value 
sys.exit(1)

