# -*- coding: utf-8 -*-
 
# Envio de archivos: cliente
# 11Sep
 
import socket
import os
 
# Creamos una lista con la dirección de
# la máquina y el puerto donde
# estara a la escucha
CONEXION = ("10.42.0.22", 9011)
ARCHIVO = "json/red2.json"
 
 
# Instanciamos el socket y nos
# conectamos
cliente = socket.socket()
cliente.connect(CONEXION)
 
# Abrimos el archivo en modo lectura binaria
# y leemos su contenido
with open(ARCHIVO, "rb") as archivo:
    buffer = archivo.read()
 
while True:
    # Enviamos al servidor la cantidad de bytes
    # del archivo que queremos enviar
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

