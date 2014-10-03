import tibiaclient
import versions
import binascii
import ptrace

tibiaclient = tibiaclient.TibiaClient('8.60');
tibiaclient.searchTibia();

if tibiaclient.attach() == 0:
	quit()

ip = "baiaklast.no-ip.biz"
print "ip: " + ip
ip = ip[::-1]

ip = binascii.hexlify(ip)

ips = []

for offset, _ in enumerate(ip):
	if ((offset + 16) % 16 == 0):
		ips.insert(offset/16, ip[offset:offset+16])

port = 7171

data = tibiaclient.readFromMemory(versions.Versions[tibiaclient.version]['ver_addr'])
data = hex(data)
data = binascii.unhexlify(data[2:])

data = ''.join(reversed(data))
data = data[:4]

if data == tibiaclient.version:
	print "Correct Tibia version."
else:
	quit()

for x in range(10):
	offset = 0
	for ips_ in reversed(ips):
		tibiaclient.writeToMemory(versions.Versions[tibiaclient.version]['ip_addr'] + x*versions.Versions[tibiaclient.version]['dist'] + offset, int(ips_, 16))
		offset = offset + len(ips_)/2
		print binascii.unhexlify(ips_)[::-1]

	tibiaclient.writeToMemory(versions.Versions[tibiaclient.version]['port_addr'] + x*versions.Versions[tibiaclient.version]['dist'], port)


tibiaclient.detach();

print "Done"