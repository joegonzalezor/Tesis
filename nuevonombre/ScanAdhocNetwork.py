#!/usr/bin/env python 
# 
# escaneo version 1.0 
# This program scans networks with iwlist command and stores it in a file 

import io 
import os 
import sys 
import subprocess 
import json 
import time 

#Interface through which the scan is done 
interface = "wlan0" 

filepath="/home/pi/carpeta/Tesis/" 

def createDaemon(): 
    """ 
      This function creates a daemon service that will execute the task below 
    """ 
    try: 
    # Store the Fork PID 
        pid = os.fork() 

        if pid > 0: 
            print 'PID: %d' % pid 
            pidarchivo = open(filepath+'pids/ScanAdhocNetwork.pid', 'w+') 
            print >> pidarchivo, pid 
            pidarchivo.close() 
            os._exit(0) 

    except OSError, error: 
        print 'Unable to fork. Error: %d (%s)' % (error.errno, error.strerror) 
        os._exit(1) 

    main() 

def main(): 
    while True: 
        try: 
	    file = open(filepath+'pids/ScanResult.txt', 'w+') 	                
            #the execution of "iwlist wlan0 scan" command is performed and the result is stored in the variable: out 
            proc = subprocess.Popen(["iwlist", interface, "scan"],stdout=subprocess.PIPE, universal_newlines=True) 
            out, err = proc.communicate()            
            #If there was an error in reading and the variable out is empty, nothing is stored in the file 
 	    if out!="": 
                print >> file, out           
	    if os.path.exists(filepath+"pids/ScanAnalysis.pid")==False: 
	        os.system("python "+filepath+"/ScanAnalysis.py") 
            #Here the errors are usually the type of file and are usually fixed once collected the file is updated 
        except: 
            print("There is an error in the file") 
	    print("Unexpected error:", sys.exc_info()[0]) 
	    raise 
            #The file is closed so as not to cause problems by being open
        finally:      	         	 
  	     file.close()             
	     time.sleep(60) 

if __name__ == "__main__": 
    createDaemon() 
