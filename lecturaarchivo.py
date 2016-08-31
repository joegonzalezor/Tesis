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

# Aqui hay un diccionario de regla que se aplicaran a la descripcion de cada celda 
# la llave la cual sera el nombre con el cual se recorreran las lineas para obtener 
# nombres de las redes y el modo 

rules={"Name":get_name, 
       	"Mode":get_mode 
       } 

# Se escogen que lineas mostrar, se escoge el nombre de la red y el modo 

columns=["Name","Mode"] 


def matching_line(lines, keyword): 
#Retorna la primera linea que concuerda en una lista de lineas 
    for line in lines: 
        matching=match(line,keyword) 
        if matching!=None: 
            return matching 
    return None 

def match(line,keyword): 
#Si la primera parte de una linea concuerda con las palabras clave, 
#retorna el final de esa linea, de otro modo retorna None 
    line=line.lstrip() 
    length=len(keyword) 
    if line[:length] == keyword: 
        return line[length:] 
    else: 
        return None 

def parse_cell(cell): 
#Aplica las reglas al texto que describe una celda y retorna un diccionario 
    parsed_cell={} 
    for key in rules: 
        rule=rules[key] 
        parsed_cell.update({key:rule(cell)}) 
    return parsed_cell 


def redTLON(nombresredes,red): 
#Retorna la primera linea que concuerda en una lista de lineas 
    for nombre in nombresredes: 
        if nombre==red: 
            return "si"
    return None

def redMayor(nombresredes):
#Retorna la primera linea que concuerda en una lista de lineas 
    matriz=[]
    for nombre in nombresredes:
	 if nombre.startswith("TLON"):
         	matriz.append(int(nombre[4:]))
		return max(matriz)
    return 0

def createDaemon(): 
   
# Esta funcion crea un demonio que ejecutara la tarea colocada abajo 
  
  try: 
    # Almacena el Pid del script 
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
#	      try: 
#Se abre el archivo de escritura 
    	         file2 = open(camino+'pids/resultado.txt', 'w') 
#Se abre el archivo a donde se envian las redes escaneadas 
  	         file = open(camino+'pids/lista.txt', 'r')    
#Estas variables manejan la informacion del comando iwlist wlan0 scan 
                 cells=[[]] 
                 parsed_cells=[]    
#Se lee el archivo y se almacena en contenido 
                 contenido=file.read() 
#Se divide el resultado del comando mediante los saltos de linea para manejarlas mediante lineas 
                 for line in contenido.split("\n"): 
                     cell_line = match(line,"Cell ") 
                     if cell_line != None: 
                         cells.append([]) 
                         line = cell_line[-27:] 
                     cells[-1].append(line.rstrip()) 
#Se almacena el resultado de las lineas en esta variable 
                 cells=cells[1:] 
#Se envia el resultado a la rutina parsed_cells para formar un archivo en formato json 
                 for cell in cells: 
                     parsed_cells.append(parse_cell(cell)) 
#El resultado de la subrutina se maneja en formato json para un manejo mas sencillo 
                 data_string = json.dumps(parsed_cells) 
	         decoded = json.loads(data_string) 
#Se crean las variables para obtener la informacion del archivo json 
                 indice=0 
                 nombresredes=[] 
#Se guarda en la matriz nombresredes todas las redes tipo ad hoc 
                 for majorkey in decoded: 
                       for subkey, value in majorkey.iteritems(): 
                            if value=="Ad-Hoc":                            
                                     nombresredes.append(str(decoded[indice]["Name"])) 
                       indice=indice+1 
#Se imprimen en el archivo de escritura 
       	         print >> file2, nombresredes	        
#Se obtiene el nombre de la red ad hoc que se esta generando para descartar que la red escaneada es la misma 		 
		 
                 file3=open(camino+"pids/nombrered.txt","r")
                 file4=open(camino+"pids/nombrered1.txt","w")
#                 nombreredes=['TLON23', 'TLON14',"TLON64","TLON11"]
                 redadhoc=file3.readline().rstrip()
		 if nombresredes!=[]:
	                 respuesta=redTLON(nombresredes,"TLON-Adhoc")
	                 if respuesta=="si":                         
	                         print >> file4, "TLON-Adhoc"
				 file4.close()
	                         os.system("bash " + camino + "creacionred/stopadhoc")
	                         os.system("bash " + camino + "creacionred/redadhoc1.sh")			      
	                 elif respuesta==None:
	                         valornodo=int(redadhoc[4:])
	                         valorext=redMayor(nombresredes)			
	       	                 if valornodo<valorext:
	               	              print >> file4, "TLON"+str(valorext)
				      file4.close()
	                       	      os.system("bash " + camino + "creacionred/stopadhoc")
	                              os.system("bash " + camino + "creacionred/redadhoc1.sh")			      
	                         else:
	                              print >> file4, "TLON"+str(valornodo)
#			 os.system("rm " +camino+"pids/nombrered.txt")
#		 print >> file2, respuesta 
#Aqui se recogen los errores que son normalmente del tipo de archivo y que suelen arreglarse una vez se actualiza el archivo 
#              except: 
#                 print("Hay un error en el archivo de lectura") 
#		 print("Unexpected error:", sys.exc_info()[0])		  
#Se cierra el archivo para que no cause problema por estar abiertos 
#              finally:      	         	 
  	         file.close() 
                 file2.close() 
		 file3.close()
		 file4.close()
	  	 time.sleep(25) 


if __name__ == "__main__": 
    createDaemon() 

