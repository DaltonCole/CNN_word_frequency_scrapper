import csv 		# Convert to spreadsheet format
import sys
import numpy
from jarcard_similarity import jarcard_similarity
from sum_of_squares import SSE
from nltk.cluster.kmeans import KMeansClusterer # Kmeans
from nltk.cluster.util import cosine_distance, euclidean_distance # Distances (cosine, euclidean)
import matplotlib.pyplot as plt

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

article_type_numeric = [[] for i in range(NUM_CLUSTERS)]
for article in article_type:
	if article == 'technology':
		article_type_numeric[0].append(0)
		article_type_numeric[1].append(1)
		article_type_numeric[2].append(2)
		article_type_numeric[3].append(3)
		article_type_numeric[4].append(4)
	elif article == 'investing':
		article_type_numeric[0].append(1)
		article_type_numeric[1].append(2)
		article_type_numeric[2].append(3)
		article_type_numeric[3].append(4)
		article_type_numeric[4].append(0)
	elif article == 'health':
		article_type_numeric[0].append(2)
		article_type_numeric[1].append(3)
		article_type_numeric[2].append(4)
		article_type_numeric[3].append(0)
		article_type_numeric[4].append(1)
	elif article == 'travel':
		article_type_numeric[0].append(3)
		article_type_numeric[1].append(4)
		article_type_numeric[2].append(0)
		article_type_numeric[3].append(1)
		article_type_numeric[4].append(2)
	elif article == 'politics':
		article_type_numeric[0].append(4)
		article_type_numeric[1].append(0)
		article_type_numeric[2].append(1)
		article_type_numeric[3].append(2)
		article_type_numeric[4].append(3)

# Reduce varience
if reduce_var:
	from sklearn.feature_selection import VarianceThreshold
	sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
	print(len(article_word_frequency[0]))
	article_word_frequency = sel.fit_transform(article_word_frequency)
	print(len(article_word_frequency[0]))
	
article_word_frequency = numpy.array(article_word_frequency, dtype=float)

#################################################### Euclidean Kmeans ####################################################
print("EUCLIDEAN")
euclidean_k_clusters = KMeansClusterer(NUM_CLUSTERS, distance=euclidean_distance, repeats=1000)
assigned_clusters_euclidean = euclidean_k_clusters.cluster(article_word_frequency, assign_clusters=True)
print((assigned_clusters_euclidean))

### SSE
euclidean_total_SSE, euclidean_SSE = SSE(article_word_frequency, assigned_clusters_euclidean, NUM_CLUSTERS)
print(euclidean_total_SSE)
print(euclidean_SSE)

### How correct were we?
correct = [0] * 5
for a_type in range(len(article_type_numeric)):
	for ty, cluster in zip(article_type_numeric[a_type], assigned_clusters_euclidean):
		if ty == cluster:
			correct[a_type] += 1
print(correct)
print(max(correct), '%')

#################################################### Cosine Kmeans ####################################################
print("COSINE")
cosine_k_clusters = KMeansClusterer(NUM_CLUSTERS, distance=cosine_distance, repeats=1000)
assigned_clusters_cosine = cosine_k_clusters.cluster(article_word_frequency, assign_clusters=True)
print(assigned_clusters_cosine)

cosine_total_SSE, cosine_SSE = SSE(article_word_frequency, assigned_clusters_cosine, NUM_CLUSTERS)
print(cosine_total_SSE)
print(cosine_SSE)

### How correct were we?
correct = [0] * 5
for a_type in range(len(article_type_numeric)):
	for ty, cluster in zip(article_type_numeric[a_type], assigned_clusters_cosine):
		if ty == cluster:
			correct[a_type] += 1
print(correct)
print(max(correct), '%')


#################################################### Jarcard Kmeans ####################################################
print("JARCARD")
jarcard_k_clusters = KMeansClusterer(NUM_CLUSTERS, distance=jarcard_similarity, repeats=25)
assigned_clusters_jarcard = jarcard_k_clusters.cluster(article_word_frequency, assign_clusters=True)
print(assigned_clusters_jarcard)

jarcard_total_SSE, jarcard_SSE = SSE(article_word_frequency, assigned_clusters_jarcard, NUM_CLUSTERS)
print(jarcard_total_SSE)
print(jarcard_SSE)

### How correct were we?
correct = [0] * 5
for a_type in range(len(article_type_numeric)):
	for ty, cluster in zip(article_type_numeric[a_type], assigned_clusters_jarcard):
		if ty == cluster:
			correct[a_type] += 1
print(correct)
print(max(correct), '%')

























