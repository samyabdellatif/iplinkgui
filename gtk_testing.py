import subprocess

# os.listdir('/sys/class/net/')
class iface:
    iname = "null"
    itype = "null"
    istat = "null"
    ilink = "null"

def searchStr(full,part):
    if part in full:
        return True
    else:
        return False


lsOut = subprocess.run("ls -l /sys/class/net/",shell=True,stdout=subprocess.PIPE, universal_newlines=True)
lsOut_full = list(filter(None,map(str.strip, lsOut.stdout.split("\n"))))

ipLinkOut = subprocess.run("ip link",shell=True,stdout=subprocess.PIPE, universal_newlines=True)
ipLinkOut_full = list(filter(None,map(str.strip, ipLinkOut.stdout.split("\n"))))

ipAddrOut = subprocess.run("ip address",shell=True,stdout=subprocess.PIPE, universal_newlines=True)
ipAddrOut_full = list(filter(None,map(str.strip, ipAddrOut.stdout.split("\n"))))


iface_list = []
for line in lsOut_full:
    # first stage is filtering all the physical interfaces
    if searchStr(line,"pci"):
        #print("this is a physical device")
        interface = iface()
        interface.iname = line.split("/")[-1]
        #second is to check the interface type, it's either internal or external(usb)
        if searchStr(line,"usb"):
            interface.itype = "USB external"
        if interface.iname[0] == "w":
            interface.itype = "Wireless"
        if interface.iname[0] == "e":
            interface.itype = "Ethernet"

        iface_list.append(interface)

total_iface = len(iface_list)
for x in iface_list:
    print(x.iname + " " + x.itype + "\n")

print("total number of interfaces installed : " + str(total_iface))