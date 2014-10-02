import tibiaclient
import versions
import binascii
import ptrace

tibiaclient = tibiaclient.TibiaClient('8.60');
tibiaclient.searchTibia();

if tibiaclient.attach() == 0:
	exit()

ip = "127.0.0.1"
ip = binascii.hexlify(ip)

ips = []

for offset, _ in enumerate(ip):
	if ((offset + 8) % 8 == 0):
		ips.insert(offset/8, ip[offset:offset+7])

port = 7171

data = tibiaclient.readFromMemory(versions.Versions[tibiaclient.version]['ver_addr'])
data = hex(data)
data = binascii.unhexlify(data[2:])

data = ''.join(reversed(data))
data = data[:4]

if data == tibiaclient.version:
	print "Correct Tibia version."
else:
	exit()

for x in range(10):
	for ips_ in ips:
		tibiaclient.writeToMemory(versions.Versions[tibiaclient.version]['ip_addr'] + x*versions.Versions[tibiaclient.version]['dist'], int(ips_, 16))
	tibiaclient.writeToMemory(versions.Versions[tibiaclient.version]['port_addr'] + x*versions.Versions[tibiaclient.version]['dist'], port)

data = tibiaclient.readFromMemory(versions.Versions[tibiaclient.version]['ip_addr'])
tibiaclient.detach();

data = hex(data)

print "Done\n\n"
print data

data = binascii.unhexlify(data[2:])

data = ''.join(reversed(data))
print data