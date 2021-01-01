# NETUI-GTK
by Samy Abdellatif

GTK3 Graphical User Interface built on top of the pynetlinux library for managing the network interfaces in python. My goal is to keep it as simple as possible. 

**Requirements**
 - [pynetlinux](https://pypi.org/project/pynetlinux/) had been used partially as an interface to the hardware.
 - dhcpcd is requered to lease IP addresses.

this app will only show the physical interfaces and allow the simple operations.

- list pysical interfaces and thier status
- switch interfaces on/off
- connect using DHCPCD on given interface (requires the installation of dhcpcd the DHCP client daemon)
- configure non-permenant static ip with netmask
- Configure default gateway.

it requires root permissions.
