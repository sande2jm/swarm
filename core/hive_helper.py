def split_json(data, size):
	splits = []
	for i in range(size):
		transform = {}
		n = int(len(data)/size)
		if i == size - 1:
			transform.update({'images':data[i*n:]})
		else:
			transform.update({'images':data[i*n:(i*n)+n]})
		splits.append(transform)
	return splits