#!/usr/bin/env python 
# 
# version 1.0 

import io 
import os 
import sys 
import subprocess 
import json 
import time 
import moduleanalysis

filepath="/home/pi/carpeta/Tesis/" 


def createDaemon():    
# This function creates a daemon service that will execute the task below   
    try: 
        # Store the Fork PID
        pid = os.fork() 
        if pid > 0: 
            pidfile = open(filepath+'pids/ScanAnalysis.pid', 'w+') 
            print >> pidfile, pid 
            pidfile.close() 
            os._exit(0) 
    except OSError, error: 
        print 'Unable to fork. Error: %d (%s)' % (error.errno, error.strerror) 
        os._exit(1) 
    main() 

def main(): 

#    while True:               
#        try: 
            #A file is opened to save the list of ad hoc networks
    	    file2 = open(filepath+'pids/AdhocNetworks.txt', 'w') 
            #A file is opened to read the results of the command iwlist scan wlan0 
  	    file = open(filepath+'pids/ScanResult.txt', 'r')                
            #the file is read and stored in a variable
            filescan=file.read() 
            #then we get a matrix with the list of Ad hoc networks
            AdhocNetworks=moduleanalysis.main(filescan)         
            #The Ad hoc networks are printed in the file 
            print >> file2, AdhocNetworks	        
            #The name of the ad hoc network that is being generated is gotten to rule that the network is not the scanned 
            file3=open(filepath+"pids/InitialAdhocName.txt","r")
            file4=open(filepath+"pids/AdhocName.txt","w")
#            nombresredes=["TLON23","TLON14","TLON64","TLON11"]
            DeviceAdhocName=file3.readline().rstrip()
            answer=""	    
            #If there are networks in blacklist.txt file, which the node have already decided not to join, thery are discarded            
            with open(filepath+"pids/BlackList.txt", "r") as BlackList:
                NetworkBL=BlackList.readlines()
            NetworksToAnalyze=[]
            for item in AdhocNetworks:
                if item not in NetworkBL:
                    NetworksToAnalyze.append(item)	    
            if NetworksToAnalyze != []:
                #If there is an Ad hoc network called TLON-Adhoc, it will have priority, the device will make the process to 
                #exchange his information and made a decision
                answer=moduleanalysis.NetworkTLON(NetworksToAnalyze,"TLON-Adhoc")
                if answer=="yes":
                    print >> file4, "TLON-Adhoc"
                    file4.close()		    
                    moduleanalysis.CreateNetworkClient()
                #If there is not an Ad Hoc Network created, the node negotiates the name of the network and makes a decision
                #wheter get in or not
                elif answer==None:
                    NodeValue=int(DeviceAdhocName[4:])
                    NetworkValue=moduleanalysis.BigNetwork(NetworksToAnalyze)
                    if NetworkValue!=None:
                        MaxValue=max(NetworkValue)
                        if NodeValue<MaxValue:
                            #Activate the client module
                            print >> file4, "TLON"+str(MaxValue)
                            file4.close()
                            moduleanalysis.CreateNetworkClient()
                        elif NodeValue>MaxValue:
                            #Activate the server module
                            moduleanalysis.CreateNetworkServer()
                            print >> file4, DeviceAdhocName
                        else:
                            #Nothing happens
                            print >> file4, DeviceAdhocName
                    else:
                        #Nothing happens                       
                        print >> file4, DeviceAdhocName
            else:
                #Nothing happens
                print >> file4, DeviceAdhocName
        #Here the errors usually occurs because the type of file and are usually fixed once the file is updated
#        except: 
#            print("There is an error in the file") 
#            print("Unexpected error:", sys.exc_info()[0])		  
        #All the files are closed
#        finally:      	         	 
            file.close() 
            file2.close() 
            file3.close()
            file4.close()
#            time.sleep(40) 

if __name__ == "__main__": 
    createDaemon() 
