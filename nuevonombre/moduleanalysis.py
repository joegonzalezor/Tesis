#!/usr/bin/env python 
# 
# version 1.0 

import io 
import os 
import sys 
import subprocess 
import json 
import time 


filepath="/home/pi/carpeta/Tesis/" 

def get_name(cell): 
    return matching_line(cell,"ESSID:")[1:-1] 

def get_mode(cell): 
    return matching_line(cell,"Mode:") 

# Here is a dictionary rule which will apply to the description of each cell; 
#The key will be the name of the column in the table. 

rules={"Name":get_name, 
       	"Mode":get_mode 
       } 

# Lines are chosen to show the network name and the mode
columns=["Name","Mode"] 

def matching_line(lines, keyword): 
# Returns the first line that matches a list of lines 
    for line in lines: 
        matching=match(line,keyword) 
        if matching!=None: 
            return matching 
    return None 

def match(line,keyword): 
# If the first part of a line matches the keywords, 
#returns the end of that line, otherwise it returns None 
    line=line.lstrip() 
    length=len(keyword) 
    if line[:length] == keyword: 
        return line[length:] 
    else: 
        return None 

def parse_cell(cell): 
# Applies the rules to the bunch of text describing a cell and returns a corresponding dictionary 
    parsed_cell={} 
    for key in rules: 
        rule=rules[key] 
        parsed_cell.update({key:rule(cell)}) 
    return parsed_cell 

def divisioncells(filescan):
#Split the result of the scan of the interface Wlan0
    cells=[[]]
    for line in filescan.split("\n"):
        cell_line = match(line,"Cell ")
        if cell_line != None:
            cells.append([])
            line = cell_line[-27:]
        cells[-1].append(line.rstrip())
    return cells

def NetworkTLON(AdhocNetworks,AdhocName): 
#If there is an ad hoc network called TLON-Adhoc, returns "si" 
    for name in AdhocNetworks: 
        if name==AdhocName: 
            return "yes"
    return None

def BigNetwork(AdhocNetworks):
# Returns the max value of the sufix of the network, this is made 
#to set the same name to the network to establish a connection and
#exchange information
    matrix=[]
    for name in AdhocNetworks:
	 if name.startswith("TLON"):
         	matrix.append(int(name[4:]))
    if matrix!=[]:
        return matrix
    else:
        return None

def CreateNetworkClient():
#stop the network, change the essid and prepare the device to send the resources information
#    os.system("bash " + filepath + "creacionred/stopadhoc")
#    os.system("bash " + filepath + "creacionred/CreateAdhoc.sh")
    value=os.system("python " + filepath + "Client.py")    
    if value==256:
        os.system("python " + filepath + "Server.py")
    if os.path.exists(filepath+"json/NetworkResources.json") and os.path.exists(filepath+"json/NodeResources.json"):
        os.system("python " + filepath + "DecisionScoring.py")
        if os.path.exists(filepath+"pids/DecisionNode.txt"):
            os.system("python " + filepath + "DecisionClient.py")
            if os.path.exists(filepath+"pids/DecisionNetwork.txt"):
                with open(filepath + "pids/DecisionNode.txt", "r") as File:
                    decisionnode=File.readline().rstrip()
                with open(filepath + "pids/DecisionNetwork.txt", "r") as File1:
                    decisionnetwork=File1.readline().rstrip()
                if decisionnode=="yes" and decisionnetwork=="yes":
                    with open(filepath + "pids/AdhocName.txt", "r") as File2:
                        NameAdhoc=File3.readline().rstrip()
                        if NameAdhoc!="TLON-Adhoc":
                            with open(filepath + "pids/AdhocName.txt", "w") as File3:
                                print >> File3, "TLON-Adhoc"
                                os.system("bash " + filepath + "creacionred/stopadhoc")
                                os.system("bash " + filepath + "creacionred/CreateAdhoc.sh")
                else:
                    with open(filepath + "pids/InitialAdhocName.txt", "r") as File4:
                        NameNetwork=File4.readline().rstrip()
                    with open(filepath + "pids/AdhocName.txt", "w") as File5:
                        print >> File5, NameNetwork
                        os.system("bash " + filepath + "creacionred/stopadhoc")
                        os.system("bash " + filepath + "creacionred/CreateAdhoc.sh")



def CreateNetworkServer():	
#Stop the network, change the essid and prepare the device to receive information
    os.system("bash " + filepath + "creacionred/stopadhoc")
    os.system("bash " + filepath + "creacionred/CreateAdhoc.sh")
    os.system("python" + filepath + " Server.py")
    os.system("python" + filepath + " Client.py")
    if os.path.exists(filepath + "json/NetworkResources.json") and os.path.exists(filepath + "json/NodeResources.json"):
        os.system("python " + filepath + " DecisionScoring.py")
        if os.path.exists(filepath+"pids/decision.txt"):
           os.system("python " + filepath + "DecisionServer.py") 
            if os.path.exists(filepath+"pids/DecisionNetwork.txt"):
                with open(filepath + "pids/DecisionNode.txt", "r") as File:
                    decisionnode=File.readline().rstrip()
                with open(filepath + "pids/DecisionNetwork.txt", "r") as File1:
                    decisionnetwork=File1.readline().rstrip()
                if decisionnode=="yes" and decisionnetwork=="yes":
                    with open(filepath + "pids/AdhocName.txt", "w") as File2:
                        print >> File2, "TLON-Adhoc"
                        os.system("bash " + filepath + "creacionred/stopadhoc")
                        os.system("bash " + filepath + "creacionred/CreateAdhoc.sh")


def main(filescan):                
    try: 
        #These variables handle command information from the file of the scan
        cells=[[]]
        parsed_cells=[]            
        #The command output is divided by line breaks to handle them 
        cells=divisioncells(filescan)            
        #The result of the lines is stored in this variable 
        cells=cells[1:] 
        #The result is sent to the parsed_cells routine to form a json format file 
        for cell in cells: 
            parsed_cells.append(parse_cell(cell)) 
        #The result of the subroutine is handled in json format for easier handling 
        data_string = json.dumps(parsed_cells) 
        decoded = json.loads(data_string) 
        #the variables are created for json file information 
        index=0 
        AdhocNetworks=[] 
        #The ad hoc networks names  are saved in the variable AdhocNetworks
        for majorkey in decoded: 
            for subkey, mode in majorkey.iteritems(): 
                if mode=="Ad-Hoc":                            
                    AdhocNetworks.append(str(decoded[index]["Name"])) 
            index=index+1 
        #The Ad hoc networks are printed in the file
        return AdhocNetworks 
    #Here the errors usually occurs because the type of file and are usually fixed once the file is updated
    except: 
        print("There is an error in the file") 
        print("Unexpected error:", sys.exc_info()[0])		         

if __name__ == "__main__": 
    main() 
