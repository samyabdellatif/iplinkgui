
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
#from subprocess import call,run,STDOUT

# creating a dummy interface class to test the GTK functions
class dummyiF:
    IP = "None"
    def __init__(self,n,i,s):
        self.name = n
        self.ID = i
        self.stat = s
    def get_iF(self):
        return([self.name,self.ID,self.stat,self.IP])
    def set_ip(self,ip):
        self.IP = ip
    def get_ip(self):
        return self.IP
    def is_up(self):
        return True if self.stat == "UP" else False


intF_list = [dummyiF('eth0','0001','UP'),dummyiF('wlp0s1','0002','UP'),dummyiF('en0','0003','DOWN')]
intF_list[0].IP = "192.168.0.2"
print([x.name for x in intF_list])
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

            interfaceDetails = intF_list[iface].ID.ljust(10," ") + " | "\
                + intF_list[iface].name.ljust(10," ") + " | "\
                + intF_list[iface].stat.ljust(4," ")
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