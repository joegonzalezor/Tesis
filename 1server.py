# -*- coding: utf-8 -*-
 
# Envio archivos: servidor
# 11Sep
 
import socket
 
# Creamos una lista con los datos del la conexión
CONEXION = ("", 9021)
 
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
sck, addr = servidor.accept()
print "Conectado a: {0}:{1}".format(*addr)
while True:
    # Recibimos la longitud que envia el cliente
    try:
        mensajesaludo=sck.recv(1024).strip()
        print("Mensaje recibido: " + mensajesaludo)
        if mensajesaludo=="HOLA":
            sck.send("HOLA QUE TAL")
        recibido = sck.recv(1024).strip()
        if recibido:
            print "Recibido:", recibido
        # Verificamos que lo que recibimos sea un número
        # en caso que así sea, enviamos el mensaje "OK"
        # al cliente indicandole que estamos listos
        # para recibir el archivo
        if recibido.isdigit():
            sck.send("OK")
        
            # Inicializamos el contador que
            # guardara la cantidad de bytes recibidos
            buffer = 0
            # Abrimos el archivo en modo escritura binaria
            with open("json/nodo.json", "wb") as archivo:
                # Nos preparamos para recibir el archivo
                # con la longitud específica
                while (buffer <= int(recibido)):
                    data = sck.recv(1)
                    if not len(data):
                        # Si no recibimos datos
                        # salimos del bucle
                        break
                    # Escribimos cada byte en el archivo
                    # y aumentamos en uno el buffer
                    archivo.write(data)
                    buffer += 1
            
                if buffer == int(recibido):
                    print "Archivo descargado con éxito"
                else:
                    print "Ocurrió un error/Archivo incompleto"
            break
    except:
        print "Client (%s, %s) is offline" % addr
        sck.close()
        sys.exit()
        continue

print("listo")
