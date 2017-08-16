from socket import *
import fcntl
import struct
import os
import time

filepath="/home/john/Tareas/Tesis/Objetivo3/"

def createDaemon(): 
    """ 
      This function creates a daemon service that will execute the task below 
    """ 
    try: 
    # Store the Fork PID 
        pid = os.fork() 

        if pid > 0: 
            print 'PID: %d' % pid 
            pidarchivo = open(filepath+'pids/sendip.pid', 'w+') 
            print >> pidarchivo, pid 
            pidarchivo.close() 
            os._exit(0)    
    except OSError, error:
        print 'Unable to fork. Error: %d (%s)' % (error.errno, error.strerror)
        os._exit(1)

    main() 


def get_ip_address(ifname):
    s = socket(AF_INET, SOCK_DGRAM)
    return inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def main():
    IPAddress=get_ip_address('lo')
    s=socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    while True: 
        try:            
            s.sendto(IPAddress,('255.255.255.255',12345))
            print IPAddress
        #Here the errors are usually the type of file and are usually fixed once collected the file is updated 
        except: 
            print("There is an error") 
            print("Unexpected error:", sys.exc_info()[0]) 
            raise 
            #The file is closed so as not to cause problems by being open
        finally:                                              
            time.sleep(10) 

if __name__ == "__main__": 
    createDaemon() 


