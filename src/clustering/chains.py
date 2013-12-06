import pickle

def get_chains(path):
	chains = {}
	limit = 100
	with open(path, 'r') as f:
		next(f)
		deviceID = None
		previous = None
		count = 0
		for line in f:
			data = line.split(',')
			x = float(data[1])
			y = float(data[2])
			z = float(data[3])
			did = int(data[4])

			if deviceID != did:
				print did
				deviceID = did
				previous = (x,y,z)
				count = 0
				chains[deviceID] = []
			else:
				if (count < limit):
					diff = (x - previous[0], y - previous[1], z - previous[2])
					previous = (x,y,z)
					chains[deviceID].append(diff)
					count += 1
		# endfor
	# endwith
	return chains



if __name__ == '__main__':
	chains = get_chains('../../data/train.csv')
	pickle.dump(chains, open('./chains.p', 'w'))
