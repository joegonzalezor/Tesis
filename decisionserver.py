# -*- coding: utf-8 -*-

# Envio archivos: servidor
# 11Sep

import socket
import os
import sys

camino="/home/pi/carpeta/Tesis/"
# Creamos una lista con los datos del la conexión
CONEXION = ("", 9022)

servidor = socket.socket()

# Ponemos el servidor a la escucha
try:
    servidor.bind(CONEXION)
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

servidor.listen(5)
print "Escuchando {0} en {1}".format(*CONEXION)
# Aceptamos conexiones
try:
    sck, addr = servidor.accept()
except socket.error as msg:
    sck.close()
#    cliente = None
    sys.exit()

print "Conectado a: {0}:{1}".format(*addr)

with open(camino + "pids/decision.txt", "r") as archivo:
        decision=archivo.readline().rstrip()

try:
# Recibimos la longitud que envia el cliente
    recibido = sck.recv(1024).strip()
    if recibido:
        print(recibido)
        sck.send(decision)
        print(decision)
except:
    print "Client (%s, %s) is offline" % addr
    sck.close()
    sys.exit()
    
servidor.close()
sck.close()
sys.exit()

