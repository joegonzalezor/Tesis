# -*- coding: utf-8 -*-

# Exchanging greetings and resource information

import socket
import os
import sys

#  A list is created with the address of the device and the port where it will listen
Connection = ("", 9020)
#We create a Socket
server = socket.socket()
# We set the server to listen
try:
    server.bind(Connection)
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

#We accept connections
server.listen(1)
print "Listening to {0} in {1}".format(*Connection)
try:
    sck, addr = server.accept()
except socket.error as msg:
    sck.close()
    sys.exit()

print "Connected to: {0}:{1}".format(*addr)
while True:
    try:
    # We receive the message that the client is sending
        message = sck.recv(1024).strip()
        if message:
            print "Recibido:", message
        # We verify that the message is a number, then we send a "OK"
        # to indicate to the client, that we are ready to receive the file          
        if message.isdigit():
            sck.send("OK")

            # We set the counter to save the number of received bytes 
            buffer = 0
            # Abrimos el archivo en modo escritura binaria
            with open("/home/pi/carpeta/Tesis/json/NetworkResources.json", "wb") as file:
                # We prepare to receive the file with the specified lenght
                while (buffer <= int(message)):
                    data = sck.recv(1)
                    if not len(data):
                        # If we have no information, we break the loop
                        break
                    # We write each byte in the file, and we add 1 to the counter
                    file.write(data)
                    buffer += 1                
                if buffer == int(message):
                    print "Archivo descargado con éxito"
                else:
                    print "Ocurrió un error/Archivo incompleto"
            break
    except:
        print "Client (%s, %s) is offline" % addr
        sck.close()
        sys.exit()
        continue
server.close()
sck.close()
sys.exit()

