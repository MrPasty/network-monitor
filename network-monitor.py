#!/usr/bin/python3
# Purpose: Scans the network based, stores what it finds in a master list
#          and then on subsequent runs compares what is on the network with the 
#          master list and prints out if any new devices found, those new
#          devices are then added to the master list
# Depends: nmap running as root, if you cant do that then run this on your 
#          system to allow it to run with elevated
#          privileges so it can get the MAC address of the devices.
#          sudo setcap cap_net_raw,cap_net_admin,cap_net_bind_service+eip /usr/bin/nmap
#

import os.path
from os import path
import nmap


# User configurable vars
MasterList = "/tmp/network-master"
MyNetwork = "192.168.1.0/24"
Nargs = "--dns-servers 192.168.1.7 --privileged -Rsn"

nm = nmap.PortScanner()
nm.scan(hosts='%s' % MyNetwork, arguments='%s' % Nargs)
devicelist = []
newdevices = []


def scannetwork():
    for host in nm.all_hosts():
        if 'mac' in nm[host]['addresses']:
            # if we have a vendor string use that otherwise just show whats in MAC field
            if len(nm[host]['vendor']) > 0:
                for key, value in nm[host]['vendor'].items():
                    vendor = "{} {}".format(key, value) + " "
            else:
                vendor = (nm[host]['addresses']['mac']) + " "
            ip = (nm[host]['addresses']['ipv4']) + " "

        if len(nm[host].hostname()) > 0:
            devicename = ' (%s)' % (nm[host].hostname())
        else:
            devicename = ' (UNKNOWN)'
        devicelist.append(vendor + ip + devicename)


def saveoutput():
    try:
        f = open(MasterList, 'w')
    except IOError:
        print("An I/O error occurred when trying to load %s" % MasterList)
        raise
    for element in devicelist:
        f.write(element)
        f.write('\n')
    f.close()


def comparefiles():
    f = open(MasterList, 'r')
    lines = f.readlines()
    master = []
    for line in lines:
        master.append(line.split(' ')[0])
    f.close()
    # Compare first field (MAC) in current scan against MAC address in MasterList
    # if MAC not found in MasterList then print it out and store in new list ready to be saved to file
    for element in devicelist:
        if element.split(" ")[0] not in master:
            newdevices.append(element)

    # if we have some output then update master list and exit, otherwise just exit
    if newdevices:
        try:
            outfile = open(MasterList, 'a')
        except IOError:
            print("An I/O error occurred when trying to open %s" % MasterList)
            raise
        for element in newdevices:
            outfile.write(element)
            outfile.write('\n')
            print(element)
        outfile.close()
        exit(0)
    else:
        exit(0)


# Main
if path.isfile(MasterList):  # Check we have a base network scan to compare against
    scannetwork()
    comparefiles()
else:
    # This should only ever run once to generate initial master scan list
    scannetwork()
    saveoutput()
