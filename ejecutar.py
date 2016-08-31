import os
camino="/home/pi/carpeta/mensaje/definitivo/"
valor=os.system("python 4client.py")
print valor
if valor==256:
    os.system("python 4server.py")
if os.path.exists(camino+"json/red2.json") and os.path.exists(camino+"json/nodo$
    os.system("python TomaDecisiones.py")

