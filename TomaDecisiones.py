import cmd
import os
import random
import math
import json


def ponderacionDD(DD):
#Ponderacion DD
        if DD<=500.0:
           ponDD=5.0
        elif DD<=1000.0:
           ponDD=4.0
        elif DD<=2000.0:
           ponDD=3.0
        elif DD<=5000.0:
           ponDD=2.0
        else:
           ponDD=1.0
	return ponDD

def ponderacion(peso):
#ponderacion Ram-Procesador-Apps
    pesosalida=0
    if peso<20.0:
       pesosalida=5.0
    elif peso<=40.0:
       pesosalida=4.0
    elif peso<=60.0:
       pesosalida=3.0
    elif peso<=80.0:
       pesosalida=2.0
    else:
       pesosalida=1.0
    return pesosalida

def pesodecision(peso,a,b,c,d,e,f,g,h):
#Funcion que normaliza los pesos para que correspondan al parametro de los pesos del criterio de Scoring
    pesosalida=0
    if peso<a:
       pesosalida=1
    elif peso<b:
       pesosalida=2
    elif peso<c:
       pesosalida=3
    elif peso<d:
       pesosalida=4
    elif peso<e:
       pesosalida=5
    elif peso<f:
       pesosalida=6
    elif peso<g:
       pesosalida=7
    elif peso<h:
       pesosalida=8
    else:
       pesosalida=9
    return pesosalida


def perifericos(perif):
    if perif=="Si":
       pond=5.0
    else:
       pond=1.0
    return pond


def arquitectura(arq):
#Se realiza la ponderacion de la arquitectura del procesador dependiendo de la familia a la cual pertenezca, 
#dependiendo de si es un computador, raspberry, beagle, celular, sensor, u otro
    if arq=="computador":
       valorarq=9.0
    elif arq=="raspberry":
       valorarq=5.0
    elif arq=="beagle":
       valorarq=6.0
    elif arq=="celular":
       valorarq=3.0
    elif arq=="sensor":
       valorarq=2.0
    else:
       valorarq=3.0
    return valorarq


def Scoring():
#variables
#Variable de ponderacion de cada criterio
	pesosnodototal=[]
	with open('json/nodo.json') as file:
                nodorecursos=json.load(file)
        with open('json/red2.json') as file2:
                redrecursos=json.load(file2)
        
#ponderacion por criterio: 1=muy poco importante, 2=poco importante, 3=importancia media, 4=algo importante, 5=muy importante
#Disco duro=5, Ram=5, Procesador=5, Bateria=5, Microfono=1, Altavoces=1, camara=1, pantalla=1, teclado=1, apps=4 
#servicios=4, Sensores=1, internet=4

#1. Se obtiene la ponderacion del recurso para el nodo

#Ponderacion disco duro
	ponDD=ponderacionDD(nodorecursos['DD']['Libre'])

#Ponderacion Ram
	ponRam=ponderacion(nodorecursos['Ram']['Libre']*100.0/nodorecursos['Ram']['Total'])

#ponderacion Bateria
	ponBat=ponderacion(nodorecursos['DD']['Libre'])
        
#ponderacion Procesador
	ponProc=ponderacion(nodorecursos['Procesador']['procesamiento'])

#ponderacion APPs
	ponAPP=ponderacion(nodorecursos['APPs']['Total'])       

#Matriz de ponderacion de criterios
	ponderacioncriterios=[ponDD,ponRam,ponBat,ponProc,1,1,1,1,1,ponAPP,1,4]
	print(ponderacioncriterios)	

#2. Rating Satisfaccion cada alternativa

#DD, Ram, Procesador, Bateria, microfono, altavoces, camara, pantalla, teclado, APPs,  Sensores, Internet
#Se sopesa la capacidad de disco duro
#El valor se sopesa diferente, pero los pesos siguen estando en el mismo rango

#Satisfaccion Disco Duro de la red
	pesoDDr=pesodecision(redrecursos['DD']['Libre'],100,300,500,1000,2000,3000,5000,10000)

#Satisfaccion Ram de la red
	pesoRamr=pesodecision(redrecursos['Ram']['Libre'],100,200,300,500,800,1000,2000,5000)

#Satisfaccion del equipo
	pesoProcr=redrecursos['Procesador']['ponderacion']
        
#Se realiza el ranking de satisfaccion para la bateria
	pesoBatr=pesodecision(redrecursos['Bateria']['Libre'],20,30,40,50,60,70,80,90)
	
#Se realiza el ranking de satisfaccion de las  Apps
	pesoAPPsr=pesodecision(redrecursos['APPs']['Total'],2, 4, 6, 8, 10 ,12, 14, 20)

#Se realiza el ranking de satisfaccion de los perifericos y el servicio de internet

	microfonor=perifericos(redrecursos['Perifericos'][0]['Disponible'])
	parlantesr=perifericos(redrecursos['Perifericos'][1]['Disponible'])
	camarar=perifericos(redrecursos['Perifericos'][2]['Disponible'])
	pantallar=perifericos(redrecursos['Perifericos'][3]['Disponible'])
	teclador=perifericos(redrecursos['Perifericos'][4]['Disponible'])
	sensoresr=perifericos(redrecursos['Perifericos'][5]['Disponible'])
	Internetr=perifericos(redrecursos['internet']['Disponible'])

#Se realiza la matriz para realizar las acciones matematicas y encontrar la decision
	pesosred=[pesoDDr,pesoRamr,pesoBatr,pesoProcr,microfonor,parlantesr,camarar,pantallar,teclador,pesoAPPsr,sensoresr,Internetr]
	
#Se realiza el mismo procedimiento anterior para el nodo

#Se realiza la ponderacion en pesos de la arquitectura del nodo
	pesoProcn=arquitectura(nodorecursos['Procesador']['Nombre'])
        
#Se sopesa la capacidad de disco duro
	pesoDDn=pesodecision(nodorecursos['DD']['Libre'],100,300,500,1000,2000,5000,7000,10000)

#Se solicita la Ram
	pesoRamn=pesodecision(nodorecursos['Ram']['Libre'],100,200,300,500,800,1000,2000,5000)

#Se realiza la ponderacion de la bateria del nodo
	pesoBatn=pesodecision(nodorecursos['Bateria']['Libre'],20,30,40,50,60,70,80,90)

#Se realiza la ponderacion de las APPs en el nodo
	pesoAppsn=pesodecision(nodorecursos['APPs']['Total'],2, 4, 6, 8, 10 ,12, 14, 20)

#Si esta bien de recursos procede a tomar la decision con la informacion que le otorgan
#Se multiplica el indice de egoismo por el peso de los nodos

	microfonon=perifericos(nodorecursos['Perifericos'][0]['Disponible'])
	parlantesn=perifericos(nodorecursos['Perifericos'][1]['Disponible'])
	camaran=perifericos(nodorecursos['Perifericos'][2]['Disponible'])
	pantallan=perifericos(nodorecursos['Perifericos'][3]['Disponible'])
	tecladon=perifericos(nodorecursos['Perifericos'][4]['Disponible'])
	sensoresn=perifericos(nodorecursos['Perifericos'][5]['Disponible'])

	Internetn=perifericos(nodorecursos['internet']['Disponible'])

#Se realiza la matriz para realizar las acciones matematicas y encontrar la decision de acuerdo al metodo Scoring

	pesosnodototal1=[pesoDDn,pesoRamn,pesoBatn,pesoProcn,microfonon,parlantesn,camaran,pantallan,tecladon,pesoAppsn,sensoresn,Internetn]

	print(pesosred)
	print(pesosnodototal1)

#Se calcula el indice de egoismo del dispositivo

	indiceegoismo=random.betavariate(4,5)
	print("el indicador de egoismo es :" + str(indiceegoismo))


#Se aplica el metodo de Scoring
	sumascoringred=0
	sumascoringnodo=0
	b=0
	for i in ponderacioncriterios:
		sumascoringred=ponderacioncriterios[b]*pesosred[b]+sumascoringred
		sumascoringnodo=ponderacioncriterios[b]*pesosnodototal1[b]+sumascoringnodo
		b=b+1
	sumascoring2=sumascoringnodo*2*indiceegoismo
	print(sumascoringred)
	print(sumascoring2)
#si el criterio de Si, da mayor que el de no, el nodo ingresara a la red ad hoc
	decisionred=1/(1+math.exp(-(sumascoringred-sumascoringnodo*indiceegoismo*2)))
	if decisionred>0.5:
	        print("El nodo decidio ingresar a la red Ad Hoc")
	else:
        	print("El nodo decidio no ingresar a la red Ad Hoc")
   
if __name__ == '__main__':
    Scoring()

