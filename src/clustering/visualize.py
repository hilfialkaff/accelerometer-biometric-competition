import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pickle
import random

def generate_colors():
	colors = []
	r = lambda: random.randint(120,255)
	for index in range(20):
		c = '#%02X%02X%02X' % (r(),r(),r())
		if not c in colors:
			colors.append(c)
	# endfor
	return colors


if __name__=='__main__':
	clusters = pickle.load(open('./clusters.p', 'r'))
	chains = pickle.load(open('./chains.p', 'r'))

	fig = plt.figure()
	ax = Axes3D(fig)
	colors = generate_colors()
	c_index = 0
	for cluster in clusters:
		for did in cluster:
			chain = chains[did]
			xs = [x for (x,y,z) in chain]
			ys = [y for (x,y,z) in chain]
			zs = [z for (x,y,z) in chain]
			ax.scatter(xs, ys, zs, c=colors[c_index], marker='o')
			# endfor
		# endfor
		c_index += 1
	# endfor
	ax.set_xlabel('X Label')
	ax.set_ylabel('Y Label')
	ax.set_zlabel('Z Label')

	plt.show()
