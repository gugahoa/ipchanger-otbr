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

		hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
		self.model = Gtk.ListStore(int, int)
		self.client_list = Gtk.ComboBox.new_with_model(self.model)
		self.client_list.connect("changed", self.selectClient)

		self.client_list.set_model(self.model)
		renderer_text = Gtk.CellRendererText()
		self.client_list.pack_start(renderer_text, True)
		self.client_list.add_attribute(renderer_text, "text", 1)

		self.button = Gtk.Button.new_from_icon_name(icon_name = "gtk-refresh", size = 2)
		self.button.set_tooltip_text("Update client list")
		self.button.connect("clicked", self.updateClients)

		hbox.pack_end(self.button, True, False, 0)
		hbox.pack_start(self.client_list, True, True, 0)
		vbox.pack_start(hbox, True, True, 0)

		box.pack_start(vbox, True, True, 0)

		self.button = Gtk.Button(label = "Change IP")
		self.button.connect("clicked", self.changeIp)
		box.pack_end(self.button, True, True, 0)

		self.connect("delete-event", self.closeWindow)

		self.tibia_proc = {}
		self.list = {}
		self.selected_version = 0

		self.updateClients(None)

	def selectClient(self, combo):
		tree_iter = combo.get_active_iter()
		if tree_iter != None:
			model = combo.get_model()
			self.selected_version = model[tree_iter][1]

	def updateClients(self, widget):
		self.pids = utils.find_pid_by_name("Tibia")
		if len(self.pids) > 0:
			for tpid in self.pids:
				if tpid not in self.tibia_proc:
					self.tibia_proc[tpid] = TibiaProcess(tpid)
				version = self.tibia_proc[tpid].getVersion()

				if version not in self.list:
					self.model.append([0, version])
					self.list[version] = []

				if tpid not in self.list[version]:
					self.list[version].append(tpid)
			for version, tpids in self.list.items():
				for tpid in tpids:
					if tpid not in self.pids:
						tpids.remove(tpid)
		else:
			self.list = {}
			self.tibia_proc = {}
			self.selected_version = 0

	def changeIp(self, widget):
		self.updateClients(None)
		if self.selected_version == 0 or self.list[self.selected_version] == []:
			print("No Tibia of such version open (%s)" % self.selected_version)
			return

		for tpid in self.list[self.selected_version]:
			if tpid not in self.pids:
				if tpid in self.tibia_proc:
					del self.tibia_proc[tpid]
				continue
			if tpid not in self.tibia_proc:
				self.tibia_proc[tpid] = TibiaProcess(tpid)

			self.tibia_proc[tpid].attach()
			self.tibia_proc[tpid].changeIp(self.entry.get_text())
			self.tibia_proc[tpid].changeRsa()

			self.tibia_proc[tpid].detach()

	def closeWindow(self, widget, event):
		print("Deleting existing objects")
		for proc in self.tibia_proc:
			print("Deleting object from process", proc)
			del proc

		print("Closing window.")
		Gtk.main_quit()
