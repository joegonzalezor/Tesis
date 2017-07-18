# -*- coding: utf-8 -*-
 
# This program bargain the amount of resources that the node is going to collaborate with the network
# The first that is gotten is the Scoring of the Network, the Scoring of the Node and the Selfishness-Altruism Indicator
import socket
import sys
import os 
import math

#The Zeuthen strategy of negotiation was chosen reach an agreement
#In this case the player 1 is the node which wants to get in to the network (player 2)
"""def Negotiation_TableU1X1(ScoringNetwork,SelfishnessIndicator,ScoringNode):
    U1X1= ScoringNetwork*SelfishnessIndicator+ScoringNode

def Negotiation_TableU2X2():
    U2X2= ScoringNode*(1-SelfishnessIndicator)+ScoringNetwork

def Negotiation_TableU1Y1():
    U1Y1= 0.5*ScoringNetwork+ScoringNode

def Negotiation_TableU2Y2():
    U2Y2= 0.5*ScoringNode+ScoringNetwork"""


# We create a instantiation of the socket and we connect to it
def main():

    # We create a list with the address of the server and the number of the socket
    Connection = ("172.0.0.1", 9022)
    filepath = "/home/john/Tareas/Tesis/Objetivo3/"
    # We open the files that have the infomation about the Scoring of the Node which is the base to the bargaining
    with open(filepath + "pids/ScoringNetwork.txt", "r") as File1:
        ScoringNetwork=float(File1.readline().rstrip())
    with open(filepath + "pids/ScoringNode.txt","r") as File2:
        ScoringNode=float(File2.readline().rstrip())
    with open(filepath + "pids/SelfishnessInd.txt","r") as File3:
        SelfishnessIndicator=float(File3.readline().rstrip())

    """try:
        client = socket.socket()
    except socket.error:
        print 'Failed to create socket'
        sys.exit(0)
    try:
        client.connect(Connection)
    except socket.error as msg:
        client.close()
        print("error")
        #A value is send if there is a error
        sys.exit(0)"""

    #The Zeuthen strategy of negotiation was chosen reach an agreement
    #In this case the player 1 is the node which wants to get in to the network (player 2)
    StepNegotiationNetwork=0
    StepNegotiationNode=0
    Negotiaton_Difference=0
    ValueagreedU1X1=0
    ValueagreedU2X2=0
    r1=0
    r2=0
#    while (Negotiaton_Difference>25 and (r1>0 or r2>0)):           
    while True:
        U1X1= ScoringNetwork*(SelfishnessIndicator-StepNegotiationNode)+ScoringNode
        U2X2= ScoringNode*(1-SelfishnessIndicator+StepNegotiationNode)+ScoringNetwork
        U1Y1= 0.5*ScoringNetwork+ScoringNode
        U2Y2= 0.5*ScoringNode+ScoringNetwork

        #For Zeuthen negotiation is necessary to stablish a status quo that means a point of minimal gain if a agreement is not reached
        U1X01= ScoringNode
        U2X02= ScoringNetwork

        print U1X1
        print U2X2
        print U1Y1
        print U2Y2
        #The Node do a proposition about the amount of resources of which it will contribute
        #In this case the Node start the bargaining
        #There are 2 options: Stick to the last offert, or accept the offert of the opponent

        #P12<=r1=(U1X1-U1Y1)/(U1X1-U1X01)
        #P21<=r2=(U2Y2-U2X2)/(U2Y2-U2X02)

        #r1 y r2 are the risk limit, the player will stick to his last offer if it thinks that it could be a higher gain

        r1=(U1X1-U1Y1)/(U1X1-U1X01)
        r2=(U2Y2-U2X2)/(U2Y2-U2X02)
        
        print str(r1) + " " + str(r2)        

        Negotiation_Difference=abs(U1X1-U1Y1)+abs(U2Y2-U2X2)
        #if r1<r2 then r1 do the next concession, if r2<r1, r2 do the next concession
        if r1<0 or r2<0:
            ValueagreedU1X1=U1X1
            ValueagreedU2X2=U2X2
            print str(ValueagreedU1X1) + " " + str(ValueagreedU2X2)
            break
        elif Negotiation_Difference<25:
            ValueagreedU1X1=U1X1
            ValueagreedU2X2=U2X2
            print str(ValueagreedU1X1) + " " +  str(ValueagreedU2X2)
            break
        elif r2>r1:
            StepNegotiationNode=StepNegotiationNode+0.1
        


"""try:
    #We Send the decision information
    print ("Sending decision information")
    client.send(decision)
    #We recieve the decision from the Server   
    message=client.recv(1024).strip()   
    print("Message received :" + message)    
    with open(filepath + "pids/DecisionNetwork.txt", "w") as file1:
        print >> file1, message   

except socket.error:
    #Send failed
    print 'Send failed'
    client.close()
    sys.exit(0)
print("Ok")
#If there is a error, we sent a value 
sys.exit(1)"""

if __name__ == "__main__":
    main()


