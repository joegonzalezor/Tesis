import fcntl
import struct

filepath = "/home/john/Tareas/Tesis/Objetivo3/"
from socket import *
s=socket(AF_INET, SOCK_DGRAM)
s.bind(('',12345))
m=s.recvfrom(1024)
with open(filepath + "pids/IPAddressreceived.txt", "w") as file1:
    print >> file1, m[0]   
def get_ip_address(ifname):
    s = socket(AF_INET, SOCK_DGRAM)
    return inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

IPAddress=get_ip_address('wlan0')

with open(filepath + "pids/IPAddressdevice.txt", "w") as file2:
    print >> file2, IPAddress

print m[0]
print IPAddress
