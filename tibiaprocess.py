import os
import ptrace
import binascii
import versions

class TibiaProcess:
	def __init__(self):
		self.pid = 0

	def searchTibia(self):
		process_list = os.popen("pidof -s Tibia")
		pid = process_list.readlines()

		if (pid):
			self.pid = int(pid[0])
			print "Tibia process found at " + str(self.pid)

			memory_map = open('/proc/' + str(self.pid) + '/maps', 'r')
			memory_map.readline() ##Skip one line.

			base_addr = memory_map.readline()[:8]
			print "Base addr is: " + base_addr

			self.base_addr = int(base_addr, 16)

			return self.pid

		return 0

	def attach(self):
		if (self.pid == 0):
			print "Unable to attach to Tibia process."
			return 0

		ptrace.attach(self.pid)
		print "Succesfully attached to Tibia process."

		return self.pid

	def detach(self):
		if (self.pid == 0):
			print "Unable to detach to Tibia process."
			return 0

		ptrace.detach(self.pid, 18)
		print "Succesfully detached to Tibia process."

		self.pid = 0
		return 1

	def writeToMemory(self, addr, value):
		if (self.pid == 0):
			print "Unable to write to process memory."
			return 0

		ptrace.pokedata(self.pid, self.base_addr + addr, value)

	def readFromMemory(self, addr):
		if (self.pid == 0):
			print "Unable to read from process memory."
			return 0

		return ptrace.peekdata(self.pid, self.base_addr + addr)