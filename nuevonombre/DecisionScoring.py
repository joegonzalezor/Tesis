import cmd
import os
import random
import math
import json
import sys

filepath="/home/pi/carpeta/Tesis/"

def WeighingHD(HD):
#Weighting Hard Disk
        if HD<=500.0:
           WeightHD=5.0
        elif HD<=1000.0:
           WeightHD=4.0
        elif HD<=2000.0:
           WeightHD=3.0
        elif HD<=5000.0:
           WeightHD=2.0
        else:
           WeightHD=1.0
	return WeightHD

def Weighing(value):
#Weighting Ram-Processor-APPs
    weight=0
    if value<20.0:
       weight=5.0
    elif value<=40.0:
       weight=4.0
    elif value<=60.0:
       weight=3.0
    elif value<=80.0:
       weight=2.0
    else:
       weight=1.0
    return weight

def weightdecision(value,a,b,c,d,e,f,g,h):
#Function which normalizes weights so that matches to the parameter of weights of Scoring Criteria
    weight=0
    if value<a:
       weight=1
    elif value<b:
       weight=2
    elif value<c:
       weight=3
    elif value<d:
       weight=4
    elif value<e:
       weight=5
    elif value<f:
       weight=6
    elif value<g:
       weight=7
    elif value<h:
       weight=8
    else:
       weight=9
    return weight


def peripherals(device):
#Function that assigns a value of 1 or 5 depending on whether or not the device has peripherals
    if device=="Si":
       weight=5.0
    else:
       weight=1.0
    return weight


def architecture(arq):
#The weighting is performed of the architecture of the processor depending of the type of the device, 
#depending on whether is a computer, raspberry, beagle, mobile, sensor and so on
    if arq=="computador":
       valuearq=9.0
    elif arq=="raspberry":
       valuearq=5.0
    elif arq=="beagle":
       valuearq=6.0
    elif arq=="celular":
       valuearq=3.0
    elif arq=="sensor":
       valuearq=2.0
    else:
       valuearq=3.0
    return valuearq


def Scoring():
        #Main Function

        #both files are opened, Node resources and Network Resources	
	with open(filepath + "json/NodeResources.json") as file:
                NodeResources=json.load(file)
        with open(filepath + 'json/NetworkResources.json') as file2:
                NetworkResources=json.load(file2)
        
        #Criteria Weighting: 1=very unimportant, 2=less important, 3=average importance, 4=some important, 5=very important

        #1.the weighting for the node is gotten
        #Hard Disk Weighting
	WeightHD=WeighingHD(NodeResources['DD']['Libre'])
        #Ram Weighting
	WeightRam=Weighing(NodeResources['Ram']['Libre']*100.0/NodeResources['Ram']['Total'])
        #Batery Weighting
	WeightBat=Weighing(NodeResources['DD']['Libre'])        
        #Procesador Weighting
	WeightProc=Weighing(NodeResources['Procesador']['procesamiento'])
        #APPs Weighting
	WeightAPP=Weighing(NodeResources['APPs']['Total'])       
        #Criteria Matrix Weighting
	WeightingCriteria=[WeightHD,WeightRam,WeightBat,WeightProc,1,1,1,1,1,WeightAPP,1,4]
	print(WeightingCriteria)	
        
        #2. Satisfaction Rating of each Alternative

        #HD, Ram, Processor, Battery, microphone, speakers, camera, screen, keyboard, APPs,  Sensors, Internet

        #Satisfaction Rating Network Hard Disk 
	WeightHDNet=weightdecision(NetworkResources['DD']['Libre'],100,300,500,1000,2000,3000,5000,10000)
        #Satisfaction Ram of the Network
	WeightRamNet=weightdecision(NetworkResources['Ram']['Libre'],100,200,300,500,800,1000,2000,5000)
        #Satisfaction of the processor
	WeightProcNet=NetworkResources['Procesador']['ponderacion']        
        # Satisfaction for the battery
	WeightBatNet=weightdecision(NetworkResources['Bateria']['Libre'],20,30,40,50,60,70,80,90)	
        #Satisfaction for the APPs
	WeightAPPNet=weightdecision(NetworkResources['APPs']['Total'],2, 4, 6, 8, 10 ,12, 14, 20)
        # Satisfaction of the peripherals and Internet
	microphoneNet=peripherals(NetworkResources['Perifericos'][0]['Disponible'])
	speakersNet=peripherals(NetworkResources['Perifericos'][1]['Disponible'])
	cameraNet=peripherals(NetworkResources['Perifericos'][2]['Disponible'])
	screenNet=peripherals(NetworkResources['Perifericos'][3]['Disponible'])
	keyboardNet=peripherals(NetworkResources['Perifericos'][4]['Disponible'])
	sensorsNet=peripherals(NetworkResources['Perifericos'][5]['Disponible'])
	InternetNet=peripherals(NetworkResources['internet']['Disponible'])

        #We group all the weighing in a matriz, the next step for make the decision 
	WeightNetwork=[WeightHDNet,WeightRamNet,WeightBatNet,WeightProcNet,microphoneNet,speakersNet,cameraNet,screenNet,keyboardNet,WeightAPPNet,sensorsNet,InternetNet]	
        
        #All the above procedure is done for the node
        #Satisfaction Rating for the node architecture 
	WeightProcNode=architecture(NodeResources['Procesador']['Nombre'])        
        #Hard disk weighting
	WeightHDNode=weightdecision(NodeResources['DD']['Libre'],100,300,500,1000,2000,5000,7000,10000)
        #Ram Weighting
	WeightRamNode=weightdecision(NodeResources['Ram']['Libre'],100,200,300,500,800,1000,2000,5000)
        #Battery Weighting
	WeightBatNode=weightdecision(NodeResources['Bateria']['Libre'],20,30,40,50,60,70,80,90)
        # Apps Weighting
	WeightAppsNode=weightdecision(NodeResources['APPs']['Total'],2, 4, 6, 8, 10 ,12, 14, 20)
        # Satisfaction of the peripherals and Internet
	microphoneNode=peripherals(NodeResources['Perifericos'][0]['Disponible'])
	speakersNode=peripherals(NodeResources['Perifericos'][1]['Disponible'])
	cameraNode=peripherals(NodeResources['Perifericos'][2]['Disponible'])
	screenNode=peripherals(NodeResources['Perifericos'][3]['Disponible'])
	keyboardNode=peripherals(NodeResources['Perifericos'][4]['Disponible'])
	sensorsNode=peripherals(NodeResources['Perifericos'][5]['Disponible'])
	InternetNode=peripherals(NodeResources['internet']['Disponible'])

        #We group all the weighing in a matriz, the next step for make the decision 

	WeightNode=[WeightHDNode,WeightRamNode,WeightBatNode,WeightProcNode,microphoneNode,speakersNode,cameraNode,screenNode,keyboardNode,WeightAppsNode,sensorsNode,InternetNode]

	print(WeightNetwork)
	print(WeightNode)
        #We calculate the selfishness index of the device
	SelfishnessInd=random.betavariate(4,5)
	print("The selfishness indicator :" + str(SelfishnessInd))
        #We apply the Scoring method
	NetworkScoringTotal=0
	NodeScoringTotal=0
	b=0
	for i in WeightingCriteria:
		NetworkScoringTotal=WeightingCriteria[b]*WeightNetwork[b]+NetworkScoringTotal
		NodeScoringTotal=WeightingCriteria[b]*WeightNode[b]+NodeScoringTotal
		b=b+1
	NodeScoringTotal=NodeScoringTotal*2*SelfishnessInd
	print(NetworkScoringTotal)
	print(NodeScoringTotal)
        #If the criteria of "yes", is greater than "not", the node will get in to the network
	NodeDecision=1/(1+math.exp(-(NetworkScoringTotal-NodeScoringTotal)))
        decision=""                                                             
        with open(filepath + "pids/DecisionNode.txt", "w") as file:                 
                if NodeDecision>0.5:
                        decision="Si"
                else:          
                        decision="No"
                print >> file, decision
        sys.exit()
   
if __name__ == '__main__':
    Scoring()

