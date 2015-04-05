from gi.repository import Gtk

from tibiaprocess import TibiaProcess
import utils

class Interface(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="OTBr IPChanger")

		box = Gtk.Box(spacing = 6)
		self.add(box)

		image = Gtk.Image()
		image.set_from_file("icon.png")
		box.pack_start(image, True, True, 0)

		self.label = Gtk.Label()
		self.label.set_text("IP Address:")

		self.entry = Gtk.Entry()
		self.entry.set_text("localhost")
		self.entry.set_max_length(32)

		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		box.pack_start(vbox, True, True, 0)

		vbox.pack_start(self.label, True, True, 0)
		vbox.pack_start(self.entry, True, True, 0)

		self.button = Gtk.Button(label = "Change IP")
		self.button.connect("clicked", self.changeIp)
		box.pack_end(self.button, True, True, 0)

		self.connect("delete-event", self.closeWindow)
		self.tibia_proc = None

	def changeIp(self, widget):
		pid = utils.find_pid_by_name("Tibia")
		if len(pid) > 0:
			tpid = pid.pop()
			if not self.tibia_proc or tpid != self.tpid:
				self.tibia_proc = TibiaProcess(tpid)
				self.tpid = tpid

			self.tibia_proc.attach()
			self.tibia_proc.changeIp(self.entry.get_text())
			self.tibia_proc.changeRsa()

			self.tibia_proc.detach()
		else:
			print("No Tibia process found!")

	def closeWindow(self, widget, event):
		print("Closing window.")
		Gtk.main_quit()
