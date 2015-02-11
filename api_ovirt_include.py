#! /usr/bin/python

# Created by Jens Depuydt
# http://www.jensd.be
# http://github.com/jensdepuydt

#this script requires ovirt-engine-sdk-python

from ovirtsdk.api import API
from ovirtsdk.xml import params
from time import sleep

def connectToHost(host,host_user,host_pw):
    apiurl="https://"+host+"/api"
    #insecure -> skips SSL check
    api = API(url=apiurl,username=host_user,password=host_pw,insecure=True)
    return api

def createGuest(api,guest_cluster,guest_name,guest_description,guest_mem,guest_cpu,guest_disk_gb,guest_domain,guest_network):
    cpu_params = params.CPU(topology=params.CpuTopology(cores=guest_cpu))
    try:
        api.vms.add(params.VM(name=guest_name,memory=guest_mem*1024*1024,cluster=api.clusters.get(guest_cluster),template=api.templates.get('Blank'),cpu=cpu_params,type_="server",description=guest_description))
   
        api.vms.get(guest_name).nics.add(params.NIC(name='nic1', network=params.Network(name=guest_network), interface='virtio'))
        
        api.vms.get(guest_name).disks.add(params.Disk(storage_domains=params.StorageDomains(storage_domain=[api.storagedomains.get(guest_domain)]),size=guest_disk_gb*1024*1024*1024,status=None,interface='virtio',format='cow',sparse=True,bootable=True))
        while api.vms.get(guest_name).status.state != 'down':
            sleep(1)
   
    except Exception as e:
        print 'Failed to create VM with disk and NIC\n%s' % str(e)

    disk_name=guest_name+"_Disk1"
    print "Waiting for "+disk_name+" to reach ok status"
    while api.vms.get(guest_name).disks.get(name=disk_name).status.state != 'ok':
        sleep(1)

    return "Succesfully created guest: "+guest_name
    
def getMac(api,guest_name):
    return api.vms.get(guest_name).nics.get("nic1").mac.address

def powerOnGuest(api,guest_name):
    try:
        if api.vms.get(guest_name).status.state != 'up':
            print 'Starting VM'
            api.vms.get(guest_name).start()
            print 'Waiting for VM to reach Up status'
            while api.vms.get(guest_name).status.state != 'up':
                sleep(1)
        else:
            print 'VM already up'
    except Exception as e:
        print 'Failed to Start VM:\n%s' % str(e)
