"""
Main routine of netui-gtk3.
:Copyright: © 2020, Samy Abdellatif.
:License: MIT.
"""
from netui import *


def main():
    win = netUImainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
if __name__ == '__main__':
    main()