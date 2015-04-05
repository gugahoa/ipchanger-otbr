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
		self.label.set_text("IP:")

		self.entry = Gtk.Entry()
		self.entry.set_text("localhost")
		self.entry.set_max_length(32)

		vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 3)
		vbox.pack_start(hbox, True, True, 0)

		hbox.pack_start(self.label, True, True, 0)
		hbox.pack_start(self.entry, True, True, 0)

		self.model = Gtk.ListStore(int, str)
		self.client_list = Gtk.ComboBox.new_with_model(self.model)
		self.client_list.connect("changed", self.selectClient)

		self.client_list.set_model(self.model)
		renderer_text = Gtk.CellRendererText()
		self.client_list.pack_start(renderer_text, True)
		self.client_list.add_attribute(renderer_text, "text", 1)

		vbox.pack_start(self.client_list, False, False, 0)

		box.pack_start(vbox, True, True, 0)

		self.button = Gtk.Button(label = "Change IP")
		self.button.connect("clicked", self.changeIp)
		box.pack_end(self.button, True, True, 0)

		self.connect("delete-event", self.closeWindow)
		self.tibia_proc = {}
		self.inserted = {}
		self.tpid = 0

		self.updateClients()

	def selectClient(self, combo):
		tree_iter = combo.get_active_iter()
		if tree_iter != None:
			model = combo.get_model()
			self.tpid = model[tree_iter][0]

			self.updateClients()
			if self.tpid not in self.pids:
				if self.tpid in self.tibia_proc:
					del self.tibia_proc[self.tpid]
				if self.tpid in self.inserted:
					del self.inserted[self.tpid]

				self.tpid = 0
				model.remove(tree_iter)

	def updateClients(self):
		self.pids = utils.find_pid_by_name("Tibia")
		if len(self.pids) > 0:
			for tpid in self.pids:
				if tpid not in self.inserted:
					self.model.append([tpid, "Tibia"])
					self.inserted[tpid] = True
		else:
			self.model.append([0, "Tibia not found"])

	def changeIp(self, widget):
		self.pids = utils.find_pid_by_name("Tibia")
		if self.tpid == 0 or self.tpid not in self.pids:
			self.updateClients()
			return

		if self.tpid not in self.tibia_proc:
			self.tibia_proc[self.tpid] = TibiaProcess(self.tpid)

		self.tibia_proc[self.tpid].attach()
		self.tibia_proc[self.tpid].changeIp(self.entry.get_text())
		self.tibia_proc[self.tpid].changeRsa()

		self.tibia_proc[self.tpid].detach()

	def closeWindow(self, widget, event):
		print("Deleting existing objects")
		for proc in self.tibia_proc:
			print("Deleting object from process", proc)
			del proc

		print("Closing window.")
		Gtk.main_quit()
