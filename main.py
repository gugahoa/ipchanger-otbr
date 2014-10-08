from ptrace.debugger.process import PtraceProcess
from ptrace.debugger.debugger import PtraceDebugger
from ptrace.debugger.memory_mapping import MemoryMapping
from sys import argv
from gi.repository import Gtk

import tibiaprocess
import utils
import interface

if __name__ == '__main__':
	pid = utils.find_pid_by_name('Tibia')
	if len(pid) > 0:
		tpid = pid.pop()
		process = tibiaprocess.TibiaProcess(tpid)

		window = interface.Interface(process)
		window.show_all()
		Gtk.main()
	else:
		print('No Tibia process found!')