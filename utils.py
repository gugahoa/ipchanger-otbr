def string_to_blocks(string, block_size):
	return_list = []
	for offset, _ in enumerate(string):
		if (offset+block_size) % block_size == 0:
			return_list.insert(offset/block_size, string[offset:offset+block_size])

	return return_list