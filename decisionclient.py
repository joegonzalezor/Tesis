# -*- coding: utf-8 -*-
 
# Envio de archivos: cliente
# 11Sep
 
import socket
import sys
import os
 
# Creamos una lista con la dirección de
# la máquina y el puerto donde
# estara a la escucha
CONEXION = ("10.42.0.21", 9022)
ARCHIVO = "/home/pi/carpeta/Tesis/pids/decision.txt"
 
#print("estoy aqui") 
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
    print("error aqui")
#    cliente = None
    sys.exit(0)
# Abrimos el archivo en modo lectura binaria
# y leemos su contenido
with open(ARCHIVO, "r") as archivo:
    decision=archivo.readline().rstrip()
 
#while True:
    # Enviamos al servidor la cantidad de bytes
    # del archivo que queremos enviar
#    print "Enviando Hola"
try:
    print ("enviando decision")
    cliente.send(decision)
    mensajerecibido=cliente.recv(1024).strip()
    print("Mensaje recibido :" + mensajerecibido)
    print "Decision"
    cliente.send(decision)    
    # Esperamos la respuesta del servidor
    recibido = cliente.recv(10)
except socket.error:
    #Send failed
    print 'Send failed'
    cliente.close()
    sys.exit(0)
print("listo")
sys.exit(1)
