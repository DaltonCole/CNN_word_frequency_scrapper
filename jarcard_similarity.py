from math import sqrt, inf
from numpy import dot

def jarcard_similarity(u, v):
	"""
	Returns the Jarcard distance between vectors u and v. Generalized Jaccard similarity and distance
	"""
	num = 0
	den = 0
	for i, j in zip(u, v):
		num += min(i, j)
		den += max(i, j)

	return 1 - (num / den)

# Other examples: http://www.nltk.org/_modules/nltk/cluster/util.html