import gi
import subprocess
import os
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from subprocess import call,run,STDOUT
from os import listdir

class interface:
    def __init__(self,n,t,s):
        self.iname = n
        self.itype = t
        self.istat = s
    def show(self):
        print(self.iname,self.itype,self.istat)

#filtering the physical interfaces only using the qdisc (scheduler), for ethernet is fq_codel
process = subprocess.run("ip link | grep -E 'qdisc fq_codel' | cut -d : -f 2", shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
intFace_ether = list(filter(None,map(str.strip, process.stdout.split("\n"))))
intF_list = []
for i in range(len(intFace_ether)):
    intF = interface(intFace_ether[i],"UP","Ethernet")
    intF_list.append(intF)

#filtering the physical interfaces only using the qdisc (scheduler), for wifi is mq
process = subprocess.run("ip link | grep -E 'qdisc mq' | cut -d : -f 2", shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
intFace_wireless = list(filter(None,map(str.strip, process.stdout.split("\n"))))
for i in range(len(intFace_wireless)):
    intF = interface(intFace_wireless[i],"UP","WiFi")
    intF_list.append(intF)

process = subprocess.run("ip link | grep -E 'BROADCAST,MULTICAST,UP,LOWER_UP' | cut -d : -f 2", shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
intFace_up = list(filter(None,map(str.strip, process.stdout.split("\n"))))
for i in range(len(intFace_up)):
    intF = interface(intFace_up[i],"CONNECTED","Ethernet")
    intF_list.append(intF)
for i in intF_list:
    i.show()

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="network interfaces")
        self.set_default_icon_from_file("iplinkgui.ico")
        self.set_default_size(300,300)
        self.button = Gtk.Button()
        self.button.set_label("ip address")
        self.button.set_margin_start(100)
        self.button.set_margin_end(100)
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)

    def on_button_clicked(self, widget):
        self.button.set_label("well, you have it")
        myInterfaces=os.listdir('/sys/class/net/')
        for i in myInterfaces:
            process = subprocess.run("ip link show "+i, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
            output = process.stdout
            print(output)

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()