"""
Build a Hidden Markove Model without caring about the
time of the data points.
"""
import numpy as np
import pandas as pd
from sklearn.hmm import GaussianHMM, GMMHMM

class NaiveHMM(object):
	def __init__(self, num_states, hmm_type=0, n_mix=3, n_iter=100, n_components=3):
		if hmm_type == 0:
			self._hmm = GaussianHMM(n_mix, n_iter=n_iter)
		elif hmm_type == 1: # WARNING: VERY VERY VERY SLOW
			self._hmm = GMMHMM(n_mix=n_mix, n_components=n_components, n_iter=n_iter)

	def fit(self, data):
		"""
		@param data DataFrame object containing T,X,Y,Z values.
		"""
		train = np.column_stack([data.X.tolist(), data.Y.tolist(), data.Z.tolist()])
		self._hmm.fit([train])

	def score(self, test):
		"""
		@param test DataFrame object containing T,X,Y,Z values.
		"""
		t = np.column_stack([test.X.tolist(), test.Y.tolist(), test.Z.tolist()])
		return self._hmm.score(t)

	def get_hmm(self):
		return self._hmm
