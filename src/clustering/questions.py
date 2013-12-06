from sets import Set
import pickle
import pprint
from kmeans import *

def questions(submission, qpath):
	s = Set()
	with open(submission, 'r') as f:
		next(f)
		for line in f:
			data = line.split(',')
			qid = int(data[0].strip())
			isTrue = float(data[1].strip())
			if isTrue > 0.5:
				s.add(qid)
		# end for
	# end with

	questions = {}
	with open(qpath, 'r') as f:
		next(f)
		for line in f:
			data = line.split(',')
			qid = int(data[0].strip())
			sid = int (data[1].strip())
			did = int(data[2].strip())

			if qid in s:
				questions[sid] = {'did': did, 'chain': []}
		# endfor
	# endwith
	return questions

def compute_chains(q, path):
	limit = 100
	with open(path, 'r') as f:
		next(f)
		sequenceID = None
		previous = None
		count = 0
		for line in f:
			data = line.split(',')
			x = float(data[1])
			y = float(data[2])
			z = float(data[3])
			sid = int(data[4])

			if not sid in q:
				continue

			if sequenceID != sid:
				print sid
				sequenceID = sid
				previous = (x,y,z)
				count = 0
			else:
				if count < limit:
					diff = (x - previous[0], y - previous[1], z - previous[2])
					previous = (x,y,z)
					q[sid]['chain'].append(diff)
					count += 1
				# endif
					
	# endwith
	return


def print_accuracy(q, clusters, chains):
	correct = 0
	total = 0
	for sid in q:
		if total == 1000:
			break
		print sid
		chain = q[sid]['chain']
		means = find_means(chains, clusters)
		max_sim = float('-inf')
		cluster_id = -1
		for index in range(0, len(means)):
			mean = means[index]
			sim = cosine_similarity(chain, mean)
			if (sim > max_sim):
				cluster_id = index
				max_sim = sim
		# endfor

		# check if correct
		did = q[sid]['did']
		if did in clusters[cluster_id]:
			correct += 1
		total += 1
	# endfor

	print correct, total, (float(correct)/total)*100.0



if __name__ == '__main__':
	q = pickle.load(open('./question_chains.p', 'r'))
	clusters = pickle.load(open('./clusters.p', 'r'))
	chains = pickle.load(open('./chains.p', 'r'))
	print_accuracy(q, clusters, chains)
