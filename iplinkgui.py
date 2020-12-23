import gi
import os
import subprocess
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
#from subprocess import call,run,STDOUT
from os import listdir

# list of the network interfaces
myInterfaces=os.listdir('/sys/class/net/')

'''creating an interface class that will include the physical interfaces only (no loopback or virtual)
interface attributes 
    iname: interface name
    itype: interface type (Ethernet, Wireless, USB)
    istat: insterface stat (UP or DOWN)
    ilink: connection stat (UP or DOWN)
    ipadd: the ip address (if connected Ex. 192.168.1.5/24 or "NULL" for not connected interfaces)
interface methods
    show:       print current attribute values
    set_up:     bring the interface to UP stat
    set_down:   bring the interface to DOWN stat
    connect:    bring connection stat to UP
    disconnect: bring connection stat to DOWN
'''
class interface:
    def __init__(self,n,t,s,l):
        self.iname = n
        self.itype = t
        self.istat = s
        self.ilink = l
        self.ipadd = ["NULL"]
        if self.ilink == "UP":
            shellcommand = r"ip addr show dev "+self.iname+r" | grep -E -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[0-9]{1,2}'"
            process = subprocess.run(shellcommand, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
            self.ipadd = list(filter(None,map(str.strip, process.stdout.split("\n"))))
    def show(self):
        print(self.iname,self.itype,self.istat,self.ilink,self.ipadd)
    def set_up(self):
        process = subprocess.run("ip link set " + self.iname + " up", shell=True,\
            check=True, stdout=subprocess.PIPE, universal_newlines=True)
        if(process.stdout == ""):
            print("interface statu changed successfully")
            self.istat = "UP"

# Final list of the interfaces
intF_list = []


# filter the connected interfaces only by checking layer 3 and layer 2 stats in the ip link command
process = subprocess.run("ip link | grep -E 'BROADCAST,MULTICAST,UP,LOWER_UP' | cut -d : -f 2", shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
intFace_up = list(filter(None,map(str.strip, process.stdout.split("\n"))))
for i in range(len(intFace_up)):
    intF = interface(intFace_up[i],"UNKNOWN","UP","UP")
    intF_list.append(intF)

#filtering the physical interfaces only using the qdisc (scheduler), for ethernet is fq_codel (Fair Queuing Controlled Delay)
process = subprocess.run("ip link | grep -E 'qdisc fq_codel' | cut -d : -f 2", shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
intFace_ether = list(filter(None,map(str.strip, process.stdout.split("\n"))))

for i in range(len(intFace_ether)):
    if any(x.iname == intFace_ether[i] for x in intF_list):
        for x in intF_list:
            if x.iname == intFace_ether[i]:
                intF_list[i].itype = "Ethernet"
    else:
        intF = interface(intFace_ether[i],"Ethernet","UP","DOWN")
        intF_list.append(intF)

#filtering the physical interfaces only using the qdisc (scheduler), for wifi is mq (multiqueue)
process = subprocess.run("ip link | grep -E 'qdisc mq' | cut -d : -f 2", shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
intFace_wireless = list(filter(None,map(str.strip, process.stdout.split("\n"))))
for i in range(len(intFace_wireless)):
    if any(x.iname == intFace_wireless[i] for x in intF_list):
        for x in intF_list:
            if x.iname == intFace_wireless[i]:
                intF_list[i].itype = "WiFi"
    else:
        intF = interface(intFace_wireless[i],"WiFi","UP","DOWN")
        intF_list.append(intF)

for i in intF_list:
    i.show()

total_iface = len(intF_list)
print("total number of interfaces installed : " + str(total_iface))
    
class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="network interfaces")
        # setting and icon and border
        self.set_default_icon_from_file("iplinkgui.ico")
        self.set_border_width(10)

        #defining listbox
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        for i in intF_list:

            interfaceDetails = i.iname + " | " + i.itype + " | " + i.istat + " | " + i.ilink + " | " + i.ipadd[0]
            #defining listbox row container
            row = Gtk.ListBoxRow()
            row.set_activatable(False)

            #inserting horizontal box inside the listbox row container
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            row.add(hbox)

            #inserting label and button widgets inside the horizontal box
            label = Gtk.Label(label=interfaceDetails,width_chars=50,xalign=0)
            hbox.pack_start(label,True,True,10)

            buttonLabel = "Disconnect"
            if i.ipadd == "NULL":
                buttonLabel = "Connect"

            self.button = Gtk.Button(label=buttonLabel)
            self.button.connect("clicked", self.on_button_clicked,i.iname)
            hbox.pack_start(self.button, True, True, 10)

            self.switch = Gtk.Switch()
            self.switch.props.valign = Gtk.Align.CENTER
            if i.ilink == "UP":
                self.switch.props.active = True
            hbox.pack_start(self.switch, True, False, 10)

            # adding the row to the listbox
            self.listbox.add(row)

        # adding the listbox to the window container (self)
        self.add(self.listbox)
        self.show_all()
        # self.button = list(Gtk.Button())
        # for i in range(total_iface):
        #     self.add = Gtk.Button(label=intF_list[i].iname)
        #     self.button[i].connect("clicked", self.on_button_clicked(self,intF_list[i].iname))
        #     self.box.pack_start(self.button[i],True,True,2)



    def on_button_clicked(self, widget,ifname):
        self.button.set_label("well, you have it")
        process = subprocess.run("ip link show dev "+ ifname, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        output = process.stdout
        print(output)

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()