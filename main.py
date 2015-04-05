#!/usr/bin/env python3.4
from gi.repository import Gtk

from interface import Interface

if __name__ == '__main__':
	window = Interface()
	window.show_all()
	Gtk.main()
