from math import sqrt
from numpy import dot

def jarcard_similarity(u, v):
	"""
	Returns the Jarcard distance between vectors u and v. Word existance is used instead of frequency.
	"""
	m_11 = 1
	m_01 = 0
	m_10 = 0

	for i, j in zip(u, v):
		if i != 0 and j != 0:
			m_11 += 1
		elif i != 0:
			m_01 += 1
		elif j != 0:
			m_10 += 1

	return (m_11 / (m_11 + m_01 + m_10))