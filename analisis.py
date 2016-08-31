#!/usr/bin/env python 
# 
# version 1.0 

import io 
import os 
import sys 
import subprocess 
import json 
import time 


camino="/home/pi/carpeta/Tesis/" 

def get_name(cell): 
    return matching_line(cell,"ESSID:")[1:-1] 

def get_mode(cell): 
    return matching_line(cell,"Mode:") 

# Here is a dictionary rule which will apply to the description of each cell; the key which in turn
# will be the name which will cycle through the lines for getting the network names and the mode 
rules={"Name":get_name, 
       	"Mode":get_mode 
       } 

# Lines are chosen to show the network name and the mode is chosen
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
# Applies the rules to the text that describes a cell and returns a dictionary 
    parsed_cell={} 
    for key in rules: 
        rule=rules[key] 
        parsed_cell.update({key:rule(cell)}) 
    return parsed_cell 

def divisioncells(archivo):
    cells=[[]]
    for line in archivo.split("\n"):
        cell_line = match(line,"Cell ")
        if cell_line != None:
            cells.append([])
            line = cell_line[-27:]
        cells[-1].append(line.rstrip())
    return cells

def RedTLON(nombresredes,red): 
#If there is an ad hoc network called TLON-Adhoc returns "si" 
    for nombre in nombresredes: 
        if nombre==red: 
            return "si"
    return None

def RedMayor(nombresredes):
# Returns the max value of the sufix of the network, this is made 
#to set the same name to the network
    matriz=[]
    for nombre in nombresredes:
	 if nombre.startswith("TLON"):
         	matriz.append(int(nombre[4:]))
    if matriz!=[]:
        return matriz
    else:
        return None

def CreateNetworkClient():
#stop the network, change the essid and prepare the device to send the resources information
#    os.system("bash " + camino + "creacionred/stopadhoc")
#    os.system("bash " + camino + "creacionred/redadhoc1.sh")
    valor1=os.system("python " + camino + "5cliente.py")
    print valor1
    if valor1==256:
        os.system("python " + camino + "5server.py")
    if os.path.exists(camino+"json/red2.json") and os.path.exists(camino+"json/nodo.json"):
        os.system("python " + camino + "TomaDecisiones.py")
        if os.path.exists(camino+"pids/decision.txt"):
           os.system("python " + camino + "decisionclient.py")


def CreateNetworkServer():
#Stop the network, change the essid and prepare the device so receive information
#    os.system("bash " + camino + "creacionred/stopadhoc")
#    os.system("bash " + camino + "creacionred/redadhoc1.sh")
    os.system("python" + camino + " 5server.py")
    os.system("python" + camino + " 5cliente.py")
    if os.path.exists(camino+"json/red2.json") and os.path.exists(camino+"json/nodo.json"):
        os.system("python TomaDecisiones.py")
        if os.path.exists(camino+"pids/decision.txt"):
           os.system("python " + camino + "decisionserver.py") 

def principal(archivo):                
#    try: 
        #These variables handle command information from the file of the scan
        cells=[[]]
        parsed_cells=[]            
        #The command output is divided by line breaks to handle them by lines 
        cells=divisioncells(archivo)            
        #The result of the lines is stored in this variable 
        cells=cells[1:] 
        #The result is sent to the parsed_cells routine to form a json format file 
        for cell in cells: 
            parsed_cells.append(parse_cell(cell)) 
        #The result of the subroutine is handled in json format for easier handling 
        data_string = json.dumps(parsed_cells) 
        decoded = json.loads(data_string) 
        #the variables are created for json file information 
        indice=0 
        nombresredes=[] 
        #The ad hoc networks names  are saved in the variable nombresredes
        for majorkey in decoded: 
            for subkey, value in majorkey.iteritems(): 
                if value=="Ad-Hoc":                            
                    nombresredes.append(str(decoded[indice]["Name"])) 
            indice=indice+1 
        #The Ad hoc networks are printed in the file
        return nombresredes 
    #Here the errors usually occurs because the type of file and are usually fixed once the file is updated
#    except: 
#        print("There is an error in the file") 
#        print("Unexpected error:", sys.exc_info()[0])		         

if __name__ == "__main__": 
    principal() 
