import os
camino="/home/pi/carpeta/mensaje/definitivo/"
os.system("python 3server.py")
os.system("python 3client.py")
if os.path.exists(camino+"json/red2.json")==True and os.path.exists(camino+"json/nodo.json"):
   os.system("python TomaDecisiones.py")

