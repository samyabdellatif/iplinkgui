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

import fcntl
import os
import struct

import ifconfig

# From linux/if_tun.h

# Ioctl defines
TUNSETNOCSUM  = 0x400454c8
TUNSETDEBUG   = 0x400454c9
TUNSETIFF     = 0x400454ca
TUNSETPERSIST = 0x400454cb
TUNSETOWNER   = 0x400454cc
TUNSETLINK    = 0x400454cd

# TUNSETIFF ifr flags
IFF_TUN       = 0x0001
IFF_TAP		  = 0x0002
IFF_NO_PI	  = 0x1000
IFF_ONE_QUEUE = 0x2000

class Tap(ifconfig.Interface):
    """
    An object representing a Linux tap device. This object can be used as an
    argument to select().

    See Documentation/networking/tuntap.txt in the linux kernel source for
    (some) programming information.
    """
    
    # See ifconfig.py for details of ifr struct
    def __init__(self, name=None):
        '''If name is None, the kernel will allocate a device name of the form tap#,
        where # is the lowest unused tap device number.'''
        self.fd = open("/dev/net/tun", "w+")

        if name is None:
            name = ""

        # TAP device with no packet information.
        ifreq = struct.pack("16sH", name, IFF_TAP | IFF_NO_PI)
        res = fcntl.ioctl(self.fd, TUNSETIFF, ifreq)
        self.name = struct.unpack("16sH", res)[0].strip('\x00')
        
        fcntl.ioctl(self.fd, TUNSETNOCSUM, 1)
        ifconfig.Interface.__init__(self, self.name)
    
    def persist(self):
        fcntl.ioctl(self.fd, TUNSETPERSIST, 1)
    
    def unpersist(self):
        fcntl.ioctl(self.fd, TUNSETPERSIST, 0)
    
    def fileno(self):
        return self.fd.fileno()
    
    def read(self, n):
        return os.read(self.fileno(), n)
    
    def write(self, data):
        return os.write(self.fileno(), data)
    
    def close(self):
        self.fd.close()

