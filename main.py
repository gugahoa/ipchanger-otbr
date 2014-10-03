import tibia_process
import versions
import binascii
import ptrace

tibia_process = tibia_process.TibiaProcess()
tibia_process.searchTibia()

if tibia_process.attach() == 0:
	quit()

tibia_client = tibiaclient.TibiaClient('8.60', tibia_process)

ip = "baiaklast.no-ip.biz"
print "ip: " + ip
ip = ip[::-1]

ip = binascii.hexlify(ip)

ips = []

for offset, _ in enumerate(ip):
	if ((offset + 16) % 16 == 0):
		ips.insert(offset/16, ip[offset:offset+16])

port = 7171

data = tibia_process.readFromMemory(versions.Versions[tibia_process.version]['ver_addr'])
data = hex(data)
data = binascii.unhexlify(data[2:])

data = ''.join(reversed(data))
data = data[:4]

if data == tibia_client.version:
	print "Correct Tibia version."
else:
	quit()

for x in range(10):
	offset = 0
	for ips_ in reversed(ips):
		tibia_process.writeToMemory(versions.Versions[tibia_process.version]['ip_addr'] + x*versions.Versions[tibia_process.version]['dist'] + offset, int(ips_, 16))
		offset = offset + len(ips_)/2
		print binascii.unhexlify(ips_)[::-1]

	tibia_process.writeToMemory(versions.Versions[tibia_process.version]['port_addr'] + x*versions.Versions[tibia_process.version]['dist'], port)


tibia_process.detach();

print "Done"