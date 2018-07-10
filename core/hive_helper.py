def split_json(data, size):
	splits = []
	for i in range(size):
		transform = {}
		n = int(len(data)/size)
		if i == size - 1:
			transform.update({'json':data[i*n:]})
		else:
			transform.update({'json':data[i*n:(i*n)+n]})
		splits.append(transform)
	return splits