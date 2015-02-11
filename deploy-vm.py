#!/usr/bin/python

# Created by Jens Depuydt
# http://www.jensd.be
# http://github.com/jensdepuydt

import sys
import os
import getpass
import api_vmware_include
import api_ovirt_include
import datetime
import time
import commands
import json
import urllib2
import string
import random
import crypt

def main():
    #file to read
    if len(sys.argv)==2:
        fname=sys.argv[1]
    else:
        print "Give an input file as argument..."
        sys.exit(99)

    #read contents of input file and put it in dict
    f=open(fname,"r")
    vm_list={}
    for line in f:
        line=line.strip()
        #ignore comments
        if not line.startswith("#") and line:
            if line.startswith("[") and line.endswith("]"):
                guest_name=line[1:-1]
                vm_list[guest_name]={}
                # default values, adjust or remove to spcify in the input-file
                vm_list[guest_name]["guest_dc"]="vSphere datacenter"
                vm_list[guest_name]["guest_cluster"]="oVirt cluster"
                vm_list[guest_name]["guest_ver"]="vmx-08"
                vm_list[guest_name]["guest_iso"]=""
                vm_list[guest_name]["guest_os"]="rhel6Guest"
                vm_list[guest_name]["guest_network"]="vlan99"
            else:
                key, value = line.split(":")
                vm_list[guest_name][key.strip()] = value.strip()
    f.close()

    for vm in vm_list:
        print "*"*sum((12,len(vm)))
        print "***** "+vm+" *****"
        print "*"*sum((12,len(vm)))
        vm_info=vm_list[vm]
        # set type of hypervisor in bool
	if vm_info["host_type"]=="vmware":
            vmware_host=True
        else:
            vmware_hist=False
        
        print "Type deployment: "+vm_info["host_type"]
        print " - Connect to hypervisor") 
        if 'host_pw' not in locals():
            host_pw=getpass.getpass("  enter password for user "+vm_info["user"]+" to continue: ")
	if vmware_host:
	        host_con=api_vmware_include.connectToHost(vm_info["host"],vm_info["user"],host_pw)
	else:
	        host_con=api_ovirt_include.connectToHost(vm_info["host"],vm_info["user"],host_pw)
        
        print " - Create VM on host"
        guest_name_purpose=vm
	if vmware_host:
            guest_name_purpose=vm+" ("+vm_info["purpose"]+")"
        print " - name:",guest_name_purpose
        print " - memory:",vm_info["guest_mem"],"MB"
        print " - #cpu:",vm_info["guest_cpu"]
        print " - space:",vm_info["guest_space"],"GB"
        print " - datastore:",vm_info["datastore"]
	if vmware_host:
            print " - target host:",vm_info["esx_host"]
        print " - hypervisor:",vm_info["host"]

	if vmware_host:
            res=api_vmware_include.createGuest(host_con,vm_info["guest_dc"],vm_info["esx_host"],guest_name_purpose,vm_info["guest_ver"],int(vm_info["guest_mem"]),int(vm_info["guest_cpu"]),vm_info["guest_iso"],vm_info["guest_os"],int(vm_info["guest_space"]),vm_info["datastore"],vm_info["guest_network"])
        else:
            res=api_ovirt_include.createGuest(host_con,vm_info["guest_cluster"],guest_name_purpose,vm_info["purpose"],int(vm_info["guest_mem"]),int(vm_info["guest_cpu"]),int(vm_info["guest_space"]),vm_info["datastore"],vm_info["guest_network"]
          
        print " -",res
        if res!="Succesfully created guest: "+guest_name_purpose:
            print "Finished unsuccesfully, aborting"
            host_con.disconnect()
            sys.exit(99)

        print " - Start the VM"
	if vmware_host:
            api_vmware_include.powerOnGuest(host_con,guest_name_purpose)
        else: 
            api_ovirt_include.powerOnGuest(host_con,guest_name_purpose) 

    print " - Disconnect from hypervisor" 
    host_con.disconnect()
            
if __name__ == '__main__':
        main()
