import pickle
import random, math
import pprint

def find_means(data, clusters):
	means = []
	for cluster in clusters:
		chains = []
		min_length = 9999
		for did in cluster:
			chain = data[did]
			if len(chain) < min_length:
				min_length = len(chain)
			chains.append(chain)
		# endfor

		mean_chain = []
		for index in range(0, min_length):
			mean_chain.append( (0,0,0) )
		# endfor

		for chain in chains:
			small_chain = chain[0:min_length]
			for index in range(0, min_length):
				coords = small_chain[index]
				x = (mean_chain[index][0] + coords[0])
				y = (mean_chain[index][1] + coords[1])
				z = (mean_chain[index][2] + coords[2])
				mean_chain[index] = (x,y,z)
			# endfor
		# endfor

		num_chains = len(chains)
		for index in range(0, min_length):
			#print mean_chain[index], num_chains
			x = mean_chain[index][0]/num_chains
			y = mean_chain[index][1]/num_chains
			z = mean_chain[index][2]/num_chains
			mean_chain[index] = (x,y,z)
		# endfor
		means.append(mean_chain)
	# endfor
	return means

# TODO Use cosine similarity instead
def euclidian_distance(v1,v2):
	min_length = min(len(v1), len(v2))

	distance = 0
	for index in range(0, min_length):
		point1 = v1[index]
		point2 = v2[index]


		distance += (point1[0]-point2[0])*(point1[0]-point2[0]) + (point1[1]-point2[1])*(point1[1]-point2[1]) + (point1[2]-point2[2])*(point1[2]-point2[2])
	return distance


def dot(v1,v2):
	d = 0
	for i in range(len(v1)):
		d += v1[i]*v2[i]
	return d

def norm(v):
	n = 0
	for i in range(len(v)):
		n += v[i]*v[i]
	return math.sqrt(n)

def smooth(v):
	delta = 0.00000001
	x = v[0] + delta
	y = v[1] + delta
	z = v[2] + delta
	return (x,y,z)

def cosine_similarity(v1,v2):
	min_length = min(len(v1), len(v2))

	similarity = 0
	for index in range(0, min_length):
		acc1 = smooth(v1[index])
		acc2 = smooth(v2[index])
		similarity += dot(acc1, acc2)/(norm(acc1)*norm(acc2))
	# endfor
	return similarity

def find_clusters(data, k):
	old_clusters = []
	clusters = []
	sample = random.sample(data.keys(), k)
	for key in sample:
		clusters.append([key])

	means = find_means(data, clusters)
	
	num_iterations = 0
	limit = 100
	while num_iterations < limit:
		old_clusters = clusters
		clusters = [[] for i in range(0,k)]
		for did in data:
			chain = data[did]
			cluster_id = 0
			#min_distance = float('inf')
			max_sim = float('-inf')
			for index in range(0,k):
				mean = means[index]
			#	distance = euclidian_distance(chain, mean)
			#	if distance < min_distance:
			#		min_distance = distance
			#		cluster_id = index
				sim = cosine_similarity(chain, mean)
				if (sim > max_sim):
					cluster_id = index
					max_sim = sim
			# endfor
			clusters[cluster_id].append(did)
		# endfor
		means = find_means(data, clusters)
		num_iterations += 1
	# endwhile
	for cluster in clusters:
		print len(cluster)
	return clusters

if __name__=='__main__':
	chains = pickle.load(open('./chains.p', 'r'))
	clusters = find_clusters(chains, 20)
	pickle.dump(clusters, open('./clusters.p', 'wb'))
