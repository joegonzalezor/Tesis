# -*- coding: utf-8 -*-

# Send Decision: Server
import socket
import os
import sys
import json

filepath="/home/john/Tareas/Tesis/Objetivo3/"
# We create a list with the address and the device; and the socket which it will listen
Connection = ("", 9026)

#We create a instantiation of the socket and we connect to it
server = socket.socket()

# We set the server to listen
try:
    server.bind(Connection)
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
# We accept a connection 
server.listen(1)
print "Listening to {0} in {1}".format(*Connection)
try:
    sck, addr = server.accept()
except socket.error as msg:
    sck.close()
    sys.exit()

print "Connected to: {0}:{1}".format(*addr)
#We open the file where we have saved the result of the process of decision making
with open(filepath + "pids/prueba/ScoringResultsServer.txt", "r") as file: 
        NetNegPointStr=file.readline().rstrip()

try:
# We receive the message with the information of the scores of the Node and the Network
    message = sck.recv(1024).strip()
    print message
    if message:
        data=json.loads(message)
        ScoringNetwork=float(data["Scoring_Network"])
        ScoringNode=float(data["Scoring_Node"])
        SelfishnessIndicator=float(data["SelfishnessIndicator"])
   
        print(str(ScoringNetwork)+" "+str(ScoringNode)+" "+str(SelfishnessIndicator))
        #if we receive a message, we sent a message back with the Point of Negotiation
        sck.send(NetNegPointStr)
        print(NetNegPointStr)
        
        #We create this variables to start the Negotiation
        NetNegPoint=float(NetNegPointStr)
        StepNegotiationNetwork=0
        StepNegotiationNode=0
        Negotiaton_Difference=0
        ValueagreedU1X1=0
        ValueagreedU2X2=0
        r1=0
        r2=0
        #First proposal from Node
        message2=sck.recv(1024).strip()
        U1X1=float(message2[0:5])
        U2X2= float(message2[6:11])
        U1Y1= (1-NetNegPoint+StepNegotiationNetwork)*ScoringNetwork+ScoringNode
        U2Y2= (NetNegPoint-StepNegotiationNetwork)*ScoringNode+ScoringNetwork
	
	#Point of Status Quo
	
	U1X01= ScoringNode
        U2X02= ScoringNetwork

        #r1 y r2 are the risk limit, the player will stick to his last offer if it thinks that it could be a higher gain

        r1=(U1X1-U1Y1)/(U1X1-U1X01)
        r2=(U2Y2-U2X2)/(U2Y2-U2X02)
 
        Negotiation_Difference=abs(U1X1-U1Y1)+abs(U2Y2-U2X2)

        #if the first proposal of the Node is accepted by the Network, then a agreement is reached and the Negotiation stops 
       
        if r1<0 or r2<0:
            ValueagreedU1X1=U1X1
            ValueagreedU2X2=U2X2
            print str(ValueagreedU1X1) + " " + str(ValueagreedU2X2)
            sck.send(str(ValueagreedU1X1)+" "+str(ValueagreedU2X2))                        
        elif Negotiation_Difference<25:
            ValueagreedU1X1=U1X1
            ValueagreedU2X2=U2X2
            print str(ValueagreedU1X1) + " " +  str(ValueagreedU2X2)            
            sck.send(str(ValueagreedU1X1)+" "+str(ValueagreedU2X2))                        
        else:	
            #If there is not agreement in the first proposal made by the Node, both players start to make concession
            StepNegotiationNetwork=0.1                    
            while True:            
                #U1X1= ScoringNetwork*(SelfishnessIndicator-StepNegotiationNode)+ScoringNode
                #U2X2= ScoringNode*(1-SelfishnessIndicator+StepNegotiationNode)+ScoringNetwork
                U1Y1= (1-NetNegPoint+StepNegotiationNetwork)*ScoringNetwork+ScoringNode
                U2Y2= (NetNegPoint-StepNegotiationNetwork)*ScoringNode+ScoringNetwork
   
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
                print str(r1) + " " + str(r2)        

                Negotiation_Difference=abs(U1X1-U1Y1)+abs(U2Y2-U2X2)
                #if r1<r2 then r1 do the next concession, if r2<r1, r2 do the next concession
                if r1<0 or r2<0:
                    #The proposal of the Network is choosen
                    ValueagreedU1X1=U1X1
                    ValueagreedU2X2=U2X2
                    print str(ValueagreedU1X1) + " " + str(ValueagreedU2X2)
                    sck.send(str(U1Y1)+" "+str(U2Y2))
                    break
                elif Negotiation_Difference<25:
                    #If the difference between the absolute value of the utilities is less than 25, then we choose the last proposal
                    ValueagreedU1X1=U1X1
                    ValueagreedU2X2=U2X2
                    print str(ValueagreedU1X1) + " " +  str(ValueagreedU2X2)
                    sck.send(str(U1Y1)+" "+str(U2Y2))
                    break
                elif r2>r1:
                    ##if r2>r1 then the Node make the next concession, we sent the proposal that we have and expect the node proposal
                    sck.send(str(U1Y1)+" "+str(U2Y2))                    
                    message2=sck.recv(1024).strip()
                    U1X1=float(message2[0:5])
                    U2X2= float(message2[6:11])                   

                elif r2<r1:
                    #if r1>r2 then the Node make the next concession
                    StepNegotiationNetwork= StepNegotiationNetwork+0.1
                else:                    
                    #if r1=r2, then both players must concede a little
                    sck.send(str(U1Y1)+" "+str(U2Y2))
                    message2=sck.recv(1024).strip()
                    U1X1=float(message2[0:5])
                    U2X2= float(message2[6:11])
                    StepNegotiationNetwork= StepNegotiationNetwork+0.1                    
except:
    print "Client (%s, %s) is offline" % addr
    sck.close()
    sys.exit()

    
#Everything is closed
server.close()
sck.close()
sys.exit()


