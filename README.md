# python-hypervisor-api
Here you can find some Python scripts and includes to interract with VMWare vCenter or ESX hosts and oVirt virtualization hosts.

##Prerequisites
###to use the scripts for VMWare vCenter or ESX
- install python-pip: (`sudo yum -y install python-pip` or similar for your distro)
- pip install pysphere (`sudo pip install pysphere`)

more information on my blog: [Create a new virtual machine in Vsphere with Python, Pysphere and the VMWare API](http://jensd.be/?p=370)

###to use the scripts for oVirt
- make sure you have access to the EPEL repositories (for CentOS or RHEL)
- install ovirt-engine-sdk-python: (`sudo yum -y install ovirt-engine-sdk-python` or similar for your distro)

more information on my blog: [Create a new virtual machine in oVirt with Python using the API] (http://jensd.be/?p=491)

##How to use:
- edit the defaults in deploy_vm.py
- create a textfile similar to example_ovirt.txt or example_vmware.txt
- execute `deploy_vm.py <name of the vm-definitions file>`

Multiple VM-definitions can be givin in one file. ovIrt and ESX can be combined.
The deploy_vm is rather quick/dirty, feel free to improve it :)
