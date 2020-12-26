# netui-gtk3
by Samy Abdellatif

GTK3 GUI app built on top of the pynetlinux package with some modifications for managing the network interfaces in python. My goal is to keep it as simple as possible, this app will only show the physical interfaces and allow the simple operations

- list pysical interfaces and thier status
- switching interfaces on/off
- connecting using DHCP (requires the installation of dhcpcd the DHCP client daemon)
- configuring non-permenant static ip with netmask and route.

it requires root permissions.
