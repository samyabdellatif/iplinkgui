# brctl,ifconfig,tap,route are forked from https://github.com/rlisagor/pynetlinux
# thanks for developers rlisagor Roman Lisagor, Robert Grant, and williamjoy williamjoy
# from brctl import *
from ifconfig import *
# from tap import *
# from route import *
import gi
import os
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
        lbox = Gtk.ListBox()
        lbox.set_selection_mode(Gtk.SelectionMode.NONE)

        #Header Row
        row = Gtk.ListBoxRow()
        row.set_activatable(False)

        #inserting horizontal box inside the listbox row container
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        row.add(hbox)

        #inserting label and button widgets inside the horizontal box
        label = Gtk.Label(label="interface Details",width_chars=50,xalign=0)
        hbox.pack_start(label,True,True,10)
        #inserting label and button widgets inside the horizontal box
        label = Gtk.Label(label="DOWN/UP",width_chars=10,xalign=1)
        hbox.pack_start(label,True,True,10)
        #inserting label and button widgets inside the horizontal box
        label = Gtk.Label(label="Desconnect/Connect",width_chars=20,xalign=1)
        hbox.pack_start(label,True,True,10)
        # adding the row to the listbox
        lbox.add(row)

        # Iterate throw interfaces and added one row for each 
        for iface in range(len(intF_list)):

            interfaceDetails = str(intF_list[iface].name) + " | " + str(intF_list[iface].get_mac()) + " | " + str(intF_list[iface].get_ip())
            #defining listbox row container
            row = Gtk.ListBoxRow()
            row.set_activatable(False)

            #inserting horizontal box inside the listbox row container
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            row.add(hbox)

            #inserting label and button widgets inside the horizontal box
            label = Gtk.Label(label=interfaceDetails,width_chars=40,xalign=0)
            hbox.pack_start(label,True,True,10)

                
            switch = Gtk.Switch()
            switch.connect("notify::active", self.on_UpDown_activated, iface)
            switch.props.valign = Gtk.Align.CENTER
            if intF_list[iface].is_up():
                switch.props.active = True
            else:
                switch.props.active = False
            hbox.pack_start(switch, True, False, 0)
            

            switch = Gtk.Switch()
            switch.connect("notify::active", self.on_ConDescon_activated, iface)
            switch.props.valign = Gtk.Align.CENTER
            if str(intF_list[iface].get_ip()) != "None":
                switch.props.active = True
            else:
                switch.props.active = False
            hbox.pack_start(switch, True, False, 0)

            # adding the row to the listbox
            lbox.add(row)

        # adding the listbox to the window container (self)
        self.add(lbox)
        self.show_all()


    def on_UpDown_activated(self, switch, gparam,i):
        if switch.get_active():
            state = "on"
        else:
            state = "off"
        print(intF_list[i].name,"UpDown Switch was turned", state)
    def on_ConDescon_activated(self, switch, gparam,i):
        if switch.get_active():
            state = "on"
        else:
            state = "off"
        print(intF_list[i].name,"ConDescon Switch was turned", state)

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()