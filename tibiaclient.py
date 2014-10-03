import versions
import binascii

class TibiaClient:
	def __init__(self, version, tibia_process):
		self.tibia_process = tibia_process
		self.version = version

	def checkTibiaVersion(self):
		data = self.tibia_process.readFromMemory(versions.Versions[self.version]['ver_addr'])
		data = hex(data)
		data = binascii.unhexlify(data[2:])

		data = ''.join(reversed(data))
		data = data[:4]

		if data == self.version:
			print "Correct Tibia version."
		else:
			print "Incorrect Tibia version"
			self.tibia_process.detach(self.tibia_process.pid, 18)
			quit()

	def changeIp(self, ips, port):
		for x in range(10):
			offset = 0
			for ips_ in reversed(ips):
				self.tibia_process.writeToMemory(versions.Versions[self.version]['ip_addr'] + x*versions.Versions[self.version]['dist'] + offset, int(ips_, 16))
				offset = offset + len(ips_)/2

			self.tibia_process.writeToMemory(versions.Versions[self.version]['port_addr'] + x*versions.Versions[self.version]['dist'], port)

	def changeRsa():
		print "changeRsa"