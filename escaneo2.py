#!/usr/bin/env python 
# 
# escaneo version 1.0 
# este programa escanea las redes con el comando iwlist y lo almacena en una tabla 

import io 
import os 
import sys 
import subprocess 
import json 
import time 

#interfaz mediante la cual se hace el escaneo 
interface = "wlan0" 
camino="/home/pi/carpeta/Tesis/" 

def createDaemon(): 
  """ 
      Esta funcion crea un servicio demonio que ejecutara la tarea de abajo 
  """ 
  try: 
    # Store the Fork PID 
    pid = os.fork() 

    if pid > 0: 
      print 'PID: %d' % pid 
      pidarchivo = open(camino+'pids/escaneo2.pid', 'w+') 
      print >> pidarchivo, pid 
      pidarchivo.close() 
      os._exit(0) 

  except OSError, error: 
    print 'Unable to fork. Error: %d (%s)' % (error.errno, error.strerror) 
    os._exit(1) 

  principal() 

def ejecucionlectura(): 
    os.system("python "+camino+"/lecturaarchivo.py") 

def principal(): 
    while True: 
	try: 
	   file = open(camino+'pids/lista.txt', 'w+') 
	   cells=[[]]            
#Se realiza la ejecucion del comando iwlist wlan0 scan y se almacena el resultado en la variable out 
           proc = subprocess.Popen(["iwlist", interface, "scan"],stdout=subprocess.PIPE, universal_newlines=True) 
           out, err = proc.communicate()            
#Si hubo un error en la lectura y out esta vacio, no se almacena nada en el archivo 
 	   if out!="": 
               print >> file, out           
	   if os.path.exists(camino+"pids/lecturaarchivo.pid")==False: 
	       ejecucionlectura() 
#Aqui se recogen los errores que son normalmente del tipo de archivo y que suelen arreglarse una vez se actualiza el archivo 
        except: 
             print("Hay un error en el archivo de lectura") 
	     print("Unexpected error:", sys.exc_info()[0]) 
	     raise 
#Se cierra el archivo para que no cause problema por estar abiertos 
        finally:      	         	 
  	     file.close()             
	     time.sleep(60) 

if __name__ == "__main__": 
    createDaemon() 

