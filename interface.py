from gi.repository import Gtk

class Interface(Gtk.Window):
	def __init__(self, process):
		Gtk.Window.__init__(self, title="OTBr IPChanger")

		self.tibia_proc = process

		box = Gtk.Box(spacing = 6)
		self.add(box)

		self.entry = Gtk.Entry()
		self.entry.set_text("localhost")
		self.entry.set_max_length(32)
		box.pack_start(self.entry, True, True, 0)

		self.button = Gtk.Button(label = "Change IP")
		self.button.connect("clicked", self.changeIp)
		box.pack_end(self.button, True, True, 0)

		self.connect("delete-event", Gtk.main_quit)

	def changeIp(self, widget):
		self.tibia_proc.attach()
		self.tibia_proc.changeIp(self.entry.get_text())
		self.tibia_proc.changeRsa()

		self.tibia_proc.detach()