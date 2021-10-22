# Purpose: 
Scans the network and stores what it finds in a master list and then on subsequent runs compares what is on the network with the master list and prints out if any new devices found, those new devices are then added to the master list.  This was created to be used with Node-Red and integrated in to Home Assistant, i.e schedule it to run in Node-Red and scan the network at regular interval defined by you and then if it finds a new device(s) the output can then be processed and sent as a notification through HA or Telegram etc. 

# Depends: 
python-nmap running with elevated privileges so it can obtain the MAC address of devices, to do this if you do not run it as root do the following.  

sudo setcap cap_net_raw,cap_net_admin,cap_net_bind_service+eip /usr/bin/nmap


Please feel free to fork this code, I am not a coder and this is just scratching my own itch...
