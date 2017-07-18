#!/bin/bash

##
# run as root 
##

#stop network manager to make the mesh network work

if [ -f /home/pi/carpeta/Tesis/pids/AdhocName.txt ]; then
   CADENA=$(head /home/pi/carpeta/Tesis/pids/AdhocName.txt)
else
   VARIABLE2=$(date +"%N" | cut -c 7,9)
   NOMBRE="TLON"
   CADENA="${NOMBRE}${VARIABLE2}"
   echo "${CADENA}" > /home/pi/carpeta/Tesis/pids/InitialAdhocName.txt
fi

echo "Stopping Network Manager"
if [ -f /etc/debian_version ]; then
	sudo service network-manager stop
elif [[ -f /etc/redhat-release ]] || [[ -f /etc/arch-release ]]; then
	sudo pkill NetworkManager
fi

# load the module up
echo "Loading batman-adv kernel module"
modprobe batman-adv

##
# waiting for interface to be released properly
# by network manager. sometimes resource busy error
# message pops up.
##
sleep 2

##
# note: the name of your ethernet & wireless interface
# may vary. please do ifconfig, find the proper name
# for your interfaces and change here before running
# the script.
##
#ip link set up dev eth0
ip link set mtu 1532 dev wlan0


##
# configure the wlan interface to operate with mtus of 1532(batman requires it)
#		and turn enc off to ensure it works

##
# 1532 mtu is already set above in line 28
# enc off can be moved below while changing mode to ad-hoc

#ifconfig wlan0 down
#ifconfig wlan0 mtu 1532
#iwconfig wlan0 enc off

# add the interface to the ad-hoc network - or create it.
echo "switching to ad-hoc mode - PYMESH"
ifconfig wlan0 down; iwconfig wlan0 mode ad-hoc channel 1 essid ${CADENA} ap 02:1B:55:AD:0C:02 enc off
#echo wlan0 > /proc/net/batman-adv/interfaces

# add wlan0 to the batman-adv virtual interface
# 	(so it can communicate with other batman-adv nodes)
echo "adding wireless interface to batman"
batctl if add wlan0

echo "bringing up wireless ad-hoc interface"
ifconfig wlan0 up

#echo wlan0 > /proc/net/batman-adv/interfaces
echo "bringing up bat0 interface"
ifconfig bat0 10.42.0.33 up


# look for neighbour nodes
#batctl -v 
#batctl o

echo "DONE."

