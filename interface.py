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
		self.tibia_proc = {}

	def changeIp(self, widget):
		pids = utils.find_pid_by_name("Tibia")
		if len(pids) > 0:
			print(len(pids), "Tibia process found")
			for tpid in pids:
				if tpid not in self.tibia_proc:
					self.tibia_proc[tpid] = TibiaProcess(tpid)

				self.tibia_proc[tpid].attach()
				self.tibia_proc[tpid].changeIp(self.entry.get_text())
				self.tibia_proc[tpid].changeRsa()

				self.tibia_proc[tpid].detach()
		else:
			print("No Tibia process found!")

	def closeWindow(self, widget, event):
		print("Deleting existing objects")
		for proc in self.tibia_proc:
			print("Deleting object from process", proc)
			del proc

		print("Closing window.")
		Gtk.main_quit()
