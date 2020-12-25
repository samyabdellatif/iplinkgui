# brctl,ifconfig,tap,route are forked from https://github.com/rlisagor/pynetlinux
# thanks for developers rlisagor Roman Lisagor, Robert Grant, and williamjoy williamjoy
# from brctl import *
from ifconfig import *
# from tap import *
# from route import *

for iface in list_ifs():
    # if iface.name=="eno1":
    #     if iface.is_up():
    #         iface.set_ip('192.168.0.10')
    #     else:
    #         iface.up()
    #         iface.set_ip('192.168.0.10')
    print(iface.get_ip())
    print(iface.get_stats())