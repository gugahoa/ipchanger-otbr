import tibiaprocess
import tibiaclient

import versions
import utils

import binascii
import ptrace

tibia_process = tibiaprocess.TibiaProcess()
tibia_process.searchTibia()

if tibia_process.attach() == 0:
	quit()

tibia_client = tibiaclient.TibiaClient('8.60', tibia_process)

ip = "baiaklast.no-ip.biz"
print "ip: " + ip
ip = ip[::-1]

ip = binascii.hexlify(ip)

ips = utils.string_to_blocks(ip, 16)

port = 7171

tibia_client.checkTibiaVersion()
tibia_client.changeIp(ips, port)
tibia_client.changeRsa()

tibia_process.detach();

print "Done"