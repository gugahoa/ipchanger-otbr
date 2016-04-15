#!/usr/bin/env python
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository import Gtk

from interface import Interface

if __name__ == '__main__':
	window = Interface()
	window.show_all()
	Gtk.main()
