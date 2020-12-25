# brctl,ifconfig,tap,route are forked from https://github.com/rlisagor/pynetlinux
# thanks for developers rlisagor Roman Lisagor, Robert Grant, and williamjoy williamjoy
# from brctl import *
from ifconfig import *
# from tap import *
# from route import *
import gi
import os
import subprocess
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
#from subprocess import call,run,STDOUT
from os import listdir

intF_list = list_ifs()
for iface in intF_list:
    if iface.is_up():
        if iface.name=="eno1":
            iface.down()
        print(iface.name + " interface is UP , IP ADDRESS: " + str(iface.get_ip()))
    else:
        print("interface is DOWN")

total_iface = len(intF_list)
print("total number of interfaces installed : " + str(total_iface))
    
class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="network interfaces")
        # setting and icon and border
        # self.set_default_icon_from_file("iplinkgui.ico")
        self.set_border_width(10)

        #defining listbox
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        for iface in intF_list:

            interfaceDetails = str(iface.name) + " | " + str(iface.get_mac()) + " | " + str(iface.get_ip())
            #defining listbox row container
            row = Gtk.ListBoxRow()
            row.set_activatable(False)

            #inserting horizontal box inside the listbox row container
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            row.add(hbox)

            #inserting label and button widgets inside the horizontal box
            label = Gtk.Label(label=interfaceDetails,width_chars=50,xalign=0)
            hbox.pack_start(label,True,True,10)

            if iface.is_up():
                buttonLabel = "Shut Down"
            else:
                buttonLabel = "Bring UP"

            self.button = Gtk.Button(label=buttonLabel)
            self.button.connect("clicked", self.on_button_clicked,iface.name)
            hbox.pack_start(self.button, True, True, 10)

            self.switch = Gtk.Switch()
            self.switch.props.valign = Gtk.Align.CENTER
            if str(iface.get_ip()) != "None":
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