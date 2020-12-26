'''
Copyright (c) 2009, Wurldtech Security Technologies, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
      
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
      
    * Neither the name of Wurldtech Security Technologies, Inc. nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import array
import fcntl
import os
import struct

import ifconfig

SYSFS_NET_PATH = "/sys/class/net"

# From linux/sockios.h
SIOCBRADDBR  = 0x89a0
SIOCBRDELBR  = 0x89a1
SIOCBRADDIF  = 0x89a2
SIOCBRDELIF  = 0x89a3

SIOCDEVPRIVATE = 0x89F0

# From bridge-utils if_bridge.h
BRCTL_SET_BRIDGE_FORWARD_DELAY = 8

if not os.path.isdir(SYSFS_NET_PATH):
    raise ImportError("Path %s not found. This module requires sysfs." % SYSFS_NET_PATH)


class Bridge(ifconfig.Interface):
    ''' Class representing a Linux Ethernet bridge. '''

    def __init__(self, name):
        ifconfig.Interface.__init__(self, name)


    def iterifs(self):
        ''' Iterate over all the interfaces in this bridge. '''
        if_path = os.path.join(SYSFS_NET_PATH, self.name, "brif")
        net_files = os.listdir(if_path)
        for iface in net_files:
            yield iface
        
        
    def listif(self):
        ''' List interface names. '''
        return [p for p in self.iterifs()]
        
        
    def addif(self, iface):
        ''' Add the interface with the given name to this bridge. Equivalent to
            brctl addif [bridge] [interface]. '''
        if type(iface) == ifconfig.Interface:
            devindex = iface.index
        else:
            devindex = ifconfig.Interface(iface).index
        ifreq = struct.pack('16si', self.name, devindex)
        fcntl.ioctl(ifconfig.sockfd, SIOCBRADDIF, ifreq)
        return self
        
        
    def delif(self, iface):
        ''' Remove the interface with the given name from this bridge.
            Equivalent to brctl delif [bridge] [interface]'''
        if type(iface) == ifconfig.Interface:
            devindex = iface.index
        else:
            devindex = ifconfig.Interface(iface).index
        ifreq = struct.pack('16si', self.name, devindex)
        fcntl.ioctl(ifconfig.sockfd, SIOCBRDELIF, ifreq)    
        return self

    def set_forward_delay(self, delay):
        # delay is passed to kernel in "jiffies", which seems to be 100ths of a second
        data = array.array('L', [BRCTL_SET_BRIDGE_FORWARD_DELAY, int(delay*100), 0, 0] )
        buffer, _items = data.buffer_info()
        ifreq = struct.pack('16sP', self.name, buffer)
        fcntl.ioctl(ifconfig.sockfd, SIOCDEVPRIVATE, ifreq)
        return self

    def delete(self):
        ''' Brings down the bridge interface, and removes it. Equivalent to
        ifconfig [bridge] down && brctl delbr [bridge]. '''
        self.down()
        fcntl.ioctl(ifconfig.sockfd, SIOCBRDELBR, self.name)
        return self

        
    def get_ip(self):
        ''' Bridges don't have IP addresses, so this always returns 0.0.0.0. '''
        return "0.0.0.0"
        
    
    ip = property(get_ip)


def shutdown():
    ''' Shut down bridge library '''
    ifconfig.shutdown()


def iterbridges():
    ''' Iterate over all the bridges in the system. '''
    net_files = os.listdir(SYSFS_NET_PATH)
    for d in net_files:
        path = os.path.join(SYSFS_NET_PATH, d)
        if not os.path.isdir(path):
            continue
        if os.path.exists(os.path.join(path, "bridge")):
            yield Bridge(d)


def list_bridges():
    ''' Return a list of the names of the bridge interfaces. '''
    return [br for br in iterbridges()]

    
def addbr(name):
    ''' Create new bridge with the given name '''
    fcntl.ioctl(ifconfig.sockfd, SIOCBRADDBR, name)
    return Bridge(name)


def findif(name):
    ''' Find the given interface name within any of the bridges. Return the
        Bridge object corresponding to the bridge containing the interface, or
        None if no such bridge could be found. '''
    for br in iterbridges():
        if name in br.iterifs():
            return br
    return None


def findbridge(name):
    ''' Find the given bridge. Return the Bridge object, or None if no such
        bridge could be found. '''
    for br in iterbridges():
        if br.name == name:
            return br
    return None

