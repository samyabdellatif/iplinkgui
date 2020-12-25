# brctl,ifconfig,tap,route are forked from https://github.com/rlisagor/pynetlinux
# thanks for developers rlisagor Roman Lisagor, Robert Grant, and williamjoy williamjoy
# from brctl import *
from ifconfig import *
# from tap import *
# from route import *

for iface in list_ifs():
    if iface.is_up():
        if iface.name=="eno1":
            iface.down()
        print(iface.name + " interface is UP , IP ADDRESS: " + str(iface.get_ip()))
    else:
        print("interface is DOWN")

