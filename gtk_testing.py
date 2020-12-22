import gi
import subprocess
import os
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from subprocess import call,run,STDOUT
from os import listdir

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