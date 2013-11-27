"""
Build a Hidden Markove Model without caring about the
time of the data points.
"""
import numpy as np
import pandas as pd
from sklearn.hmm import GaussianHMM, GMMHMM

class NaiveHMM(object):

	def __init__(self, num_states, hmm_type=0, n_mix=3):
		if hmm_type == 0:
			self._hmm = GaussianHMM(4, n_iter=100)
		elif hmm_type == 1:
			self._hmm = GMMHMM(n_components=3, n_mix=3, n_iter=100)

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
