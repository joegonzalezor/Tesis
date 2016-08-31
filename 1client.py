# -*- coding: utf-8 -*-
 
# Envio de archivos: cliente
# 11Sep
 
import socket
import os
import sys
 
# Creamos una lista con la dirección de
# la máquina y el puerto donde
# estara a la escucha
CONEXION = ("10.42.0.33", 9020)
ARCHIVO = "json/red2.json"
 
 
# Instanciamos el socket y nos
# conectamos

try:
    cliente = socket.socket()
except socket.error:
    print 'Failed to create socket'
    sys.exit(0)
try:
    cliente.connect(CONEXION)
except socket.error as msg:
    cliente.close()
#    cliente = None
    sys.exit(0)

 
# Abrimos el archivo en modo lectura binaria
# y leemos su contenido
with open(ARCHIVO, "rb") as archivo:
    buffer = archivo.read()
 
while True:
    # Enviamos al servidor la cantidad de bytes
    # del archivo que queremos enviar
    try:
        print "Enviando buffer"
        cliente.send(str(len(buffer)))
    
        # Esperamos la respuesta del servidor
        recibido = cliente.recv(10)
    # Enviamos al servidor la cantidad de bytes
    # del archivo que queremos enviar
    try:
        print "Enviando buffer"
        cliente.send(str(len(buffer)))
    
        # Esperamos la respuesta del servidor
        recibido = cliente.recv(10)
        if recibido == "OK":
            # En el caso que la respuesta sea la correcta
            # enviamos el archivo byte por byte
            # y salimos del while
            for byte in buffer:
                cliente.send(byte)
            break
    except socket.error:
        #Send failed
        print 'Send failed'
        cliente.close()
        sys.exit(0)
print("listo")
sys.exit(1)

