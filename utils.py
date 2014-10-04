import os

def find_pid_by_name(name):
	result = []
	pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

	for pid in pids:
		comm = open(''.join(['/proc/', pid, '/comm']), 'r')
		proc_name = comm.read().strip()

		if name == proc_name:
			result.append(int(pid))

	return result