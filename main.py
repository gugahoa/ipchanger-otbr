import tibiaprocess
import tibiaclient
import versions
import binascii
import ptrace

tibia_process = tibiaprocess.TibiaProcess()
tibia_process.searchTibia()

if tibia_process.attach() == 0:
	quit()

tibia_client = tibiaclient.TibiaClient('8.60', tibia_process)

ip = "localhost"
print "ip: " + ip
ip = ip[::-1]

ip = binascii.hexlify(ip)

ips = []

for offset, _ in enumerate(ip):
	if ((offset + 16) % 16 == 0):
		ips.insert(offset/16, ip[offset:offset+16])

port = 7171

tibia_client.checkTibiaVersion()
tibia_client.changeIp(ips, port)
tibia_client.changeRsa()

tibia_process.detach();

print "Done"