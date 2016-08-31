#!/usr/bin/env python 
# 
# version 1.0 

import io 
import os 
import sys 
import subprocess 
import json 
import time 
import analisis

camino="/home/pi/carpeta/Tesis/" 


def createDaemon():    
# This function creates a daemon service that will execute the task below   
    try: 
        # Store the Fork PID
        pid = os.fork() 
        if pid > 0: 
            pidarchivo = open(camino+'pids/lecturaarchivo.pid', 'w+') 
            print >> pidarchivo, pid 
            pidarchivo.close() 
            os._exit(0) 
    except OSError, error: 
        print 'Unable to fork. Error: %d (%s)' % (error.errno, error.strerror) 
        os._exit(1) 
    principal() 

def principal(): 

    while True:               
        try: 
            #A file is opened to save the list of ad hoc networks
    	    file2 = open(camino+'pids/resultado.txt', 'w') 
            #A file is openede to read the results of the command iwlist scan wlan0 
  	    file = open(camino+'pids/lista.txt', 'r')                
            #the file is read and stored in content 
            contenido=file.read() 
            nombresredes=analisis.principal(contenido)         
            #The Ad hoc networks are printed in the file 
            print >> file2, nombresredes	        
            #The name of the ad hoc network that is being generated is gotten to rule that the network is not the scanned 
            file3=open(camino+"pids/nombrered.txt","r")
            file4=open(camino+"pids/nombrered1.txt","w")
#            nombresredes=["TLON23","TLON14","TLON64","TLON11"]
            redadhoc=file3.readline().rstrip()
            respuesta=""	    
            if nombresredes != []:
#                print "pasamos por aqui"
                respuesta=analisis.RedTLON(nombresredes,"TLON-Adhoc")
                if respuesta=="si":
                    print >> file4, "TLON-Adhoc"
                    file4.close()
                    analisis.CreateNetworkClient()
#		    os.system("bash " + camino + "decision.py")	      
                elif respuesta==None:
                    valornodo=int(redadhoc[4:])
                    valorred=analisis.RedMayor(nombresredes)
                    if valorred!=None:
                        valorext=max(valorred)
                        if valornodo<valorext:
                            print >> file4, "TLON"+str(valorext)
                            file4.close()
                            analisis.CreateNetworkClient()
                        elif valornodo>valorext:
#                            print("activa modulo servidor")
                            analisis.CreateNetworkServer()
                            print >> file4, redadhoc
                        else:
#                            print("no pasa nada")
                            print >> file4, redadhoc
                    else:
#                        print("no pasa nada")
                        print >> file4, redadhoc
            else:
                print >> file4, redadhoc
#                print("no pasa nada")             
#			 os.system("rm " +camino+"pids/nombrered.txt")
#		 print >> file2, respuesta 
        #Here the errors usually occurs because the type of file and are usually fixed once the file is updated
        except: 
            print("There is an error in the file") 
            print("Unexpected error:", sys.exc_info()[0])		  
        #All the files are closed
        finally:      	         	 
            file.close() 
            file2.close() 
            file3.close()
            file4.close()
            time.sleep(40) 

if __name__ == "__main__": 
    createDaemon() 
