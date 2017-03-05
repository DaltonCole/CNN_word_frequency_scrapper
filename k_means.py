import csv 		# Convert to spreadsheet format
import sys
import numpy
from jarcard_similarity import jarcard_similarity
from nltk.cluster.kmeans import KMeansClusterer # Kmeans
from nltk.cluster.util import cosine_distance, euclidean_distance # Distances (cosine, euclidean)

# Flags
reduce_var = False
if '-r' in sys.argv:
	reduce_var = True

#################################################### Extract csv data ####################################################
### article_word_frequency is the word frequency in each article (only numbers)
### article_type is the type of every article
### words is what each index corresponds to

# Every row in the csv file
rows = []

# Read every row in data.csv file
with open('data.csv', 'r') as csvfile:
	reader = csv.reader(csvfile)
	rows = []
	for row in reader:
		rows.append(row)

##### Constants #####
article_count = len(rows) - 1
NUM_CLUSTERS = 5
#####################

# List of words
words = rows[0][3:]

# Frequency of every word in every article
article_word_frequency = rows[1:]
for i in range(len(article_word_frequency)):
	article_word_frequency[i] = article_word_frequency[i][3:]

# Type of every article
article_type = []
for row in rows:
	article_type.append(row[1])
article_type = article_type[1:]


# Reduce varience
if reduce_var:
	from sklearn.feature_selection import VarianceThreshold
	sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
	print(len(article_word_frequency[0]))
	article_word_frequency = sel.fit_transform(article_word_frequency)
	print(len(article_word_frequency[0]))

article_word_frequency = numpy.array(article_word_frequency, dtype=float)
#################################################### Euclidean Kmeans ####################################################
euclidean_k_clusters = KMeansClusterer(NUM_CLUSTERS, distance=euclidean_distance, repeats=25)
assigned_clusters_euclidean = euclidean_k_clusters.cluster(article_word_frequency, assign_clusters=True)
print(assigned_clusters_euclidean)

#################################################### Cosine Kmeans ####################################################
cosine_k_clusters = KMeansClusterer(NUM_CLUSTERS, distance=cosine_distance, repeats=25)
assigned_clusters_cosine = cosine_k_clusters.cluster(article_word_frequency, assign_clusters=True)
print(assigned_clusters_cosine)

#################################################### Jarcard Kmeans ####################################################
jarcard_k_clusters = KMeansClusterer(NUM_CLUSTERS, distance=jarcard_similarity, repeats=25)
assigned_clusters_jarcard = jarcard_k_clusters.cluster(article_word_frequency, assign_clusters=True)
print(assigned_clusters_jarcard)



























