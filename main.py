from ptrace.debugger.process import PtraceProcess
from ptrace.debugger.debugger import PtraceDebugger
from ptrace.debugger.memory_mapping import MemoryMapping
from sys import argv

import tibiaprocess
import utils

if __name__ == '__main__':
	pid = utils.find_pid_by_name('Tibia')
	if len(pid) > 0:
		tpid = pid.pop()
		process = tibiaprocess.TibiaProcess(tpid)
		process.attach()
		process.changeRsa()
		process.changeIp('nelvara.com')
	else:
		print('No Tibia process found!')