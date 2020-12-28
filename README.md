# NETUI-GTK
by Samy Abdellatif

GTK3 Graphical User Interface built on top of the pynetlinux library for managing the network interfaces in python. My goal is to keep it as simple as possible. 

\\Requirements
 - [pynetlinux](https://pypi.org/project/pynetlinux/) used partially as an interface to the hardware. but not requred to be installed as parts requiered are already added to the source code.
 - dhcpcd is requered to lease IP addresses.

this app will only show the physical interfaces and allow the simple operations.

- list pysical interfaces and thier status
- switching interfaces on/off
- connecting using DHCP (requires the installation of dhcpcd the DHCP client daemon)
- configuring non-permenant static ip with netmask and route.

it requires root permissions.
