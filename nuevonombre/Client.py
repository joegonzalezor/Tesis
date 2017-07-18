# -*- coding: utf-8 -*-
 
# Exchanging greetings and resource information
 
import socket
import sys
import os 
# A list is created with the address of the device and the port where it will listen
Connection = ("10.42.0.21", 9021)
file = "/home/pi/carpeta/Tesis/json/NodeResources.json" 
# We create a Socket
try:
    client = socket.socket()
except socket.error:
    print 'Failed to create socket'
    #A value is send if there is a error
    sys.exit(0)
#We connect to the server
try:
    client.connect(Connection)
except socket.error as msg:
    client.close()
    print("error")
    #We send a value if there is a error
    sys.exit(0)
    # We open the file in binary mode reading 
with open(file, "rb") as File:
    buffer = File.read()
 
while True:
    # We send to the server the number of bytes of the file that we want to send
    try:
        print ("Sending Hello")
        client.send("Hola")
        message=client.recv(1024).strip()
        print("Message Received :" + message)
        print "Sending Buffer size"
        client.send(str(len(buffer)))    
        # We wait the answer of the server
        answer = client.recv(10)
        if answer == "OK":
            # In case there is an answer from the server, we sent the file byte by byte
            # and we break the While
            
            for byte in buffer:
                client.send(byte)
            break
    except socket.error:
        #Send failed
        print 'Send failed'
        client.close()
        sys.exit(0)
print("Ready")
sys.exit(1)

