import csv 		# Convert to spreadsheet format
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import f1_score
from sklearn.feature_selection import VarianceThreshold
import numpy as np
import matplotlib.pyplot as plt
from random import sample # Random integer
import os
import sys

reduce_var = False
if '-r' in sys.argv:
	reduce_var = True

#################################################### Extract csv data ####################################################
# Every row in the csv file
rows = []

# Read every row in data.csv file
with open('data.csv', 'r') as csvfile:
	reader = csv.reader(csvfile)
	rows = []
	for row in reader:
		rows.append(row)

### Constants ###
article_count = len(rows) - 1
n_folds = 5
articles_per_fold = article_count // n_folds

# List of words
words = rows[0][3:]

tommy = words.index('verizon')

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
	sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
	print(len(article_word_frequency[0]))
	article_word_frequency = sel.fit_transform(article_word_frequency)
	print(len(article_word_frequency[0]))

#################################################### Create n-fold cross validation set ####################################################
index_cross_validation = []
randome_set = []

random_fold = sample(range(article_count), article_count)

cross_validation_data = []
cross_validation_answer = []

for index in range(n_folds):
	# Test articles
	data = []
	answer = []
	for i in range(index, article_count, n_folds):
		data.append(article_word_frequency[random_fold[i]])
		answer.append(article_type[random_fold[i]])

	cross_validation_data.append(data)
	cross_validation_answer.append(answer)

#################################################### kNN ####################################################
# kNN, 1-articles_per_fold closest neghbors
neighbor_accuracy = []
f_measure = []
flatten = lambda l: [item for sublist in l for item in sublist]
for neighbor_count in range(1, 21):#articles_per_fold + 1):
	# kNN
	sub_f_measure = []
	percent_correct = []
	for i in range(n_folds):
		# Fit Data to three closest neighbors
		neigh = KNeighborsClassifier(n_neighbors=neighbor_count)
		neigh.fit(flatten(cross_validation_data[0:i] + cross_validation_data[i+1:n_folds]), flatten(cross_validation_answer[0:i] + cross_validation_answer[i+1:n_folds]))

		perdiction = neigh.predict(cross_validation_data[i])

		# See how many kNN got right
		correct = 0
		for real, guess in zip(cross_validation_answer[i], perdiction):
			if real == guess:
				correct += 1

		percent_correct.append(correct / articles_per_fold)

		# F1-measure
		sub_f_measure.append(f1_score(cross_validation_answer[i], perdiction, average='weighted'))

	# Perdiction accuracy
	accuracy = 0
	for i in percent_correct:
		accuracy += i
	accuracy /= n_folds

	neighbor_accuracy.append(accuracy)
	f_measure.append(sub_f_measure)

x = []
y = []
print("kNN")
print("Nodes \t Percent \t F-measure")
for i in range(len(neighbor_accuracy)):
	print(i + 1, '\t', round(neighbor_accuracy[i] * 100, 1), '%', '\t', f_measure[i])
	x.append(i+1)
	y.append(round(neighbor_accuracy[i] * 100, 1))

plt.scatter(x, y)
plt.suptitle('kNN vs Percent Accuracy', fontsize=20)
plt.xlabel('kNN', fontsize=18)
plt.ylabel('Percent Accuracy', fontsize=16)
if reduce_var == False:
	plt.savefig('kNNvsNum.png')
else:
	plt.savefig('kNNvsNum_Reduced.png')

#################################################### Decision Tree ####################################################
percent_correct = []
f_measure = []
count = 0
for i in range(n_folds):
	clf = DecisionTreeClassifier()
	clf = clf.fit(flatten(cross_validation_data[0:i] + cross_validation_data[i+1:n_folds]), flatten(cross_validation_answer[0:i] + cross_validation_answer[i+1:n_folds]))

	perdiction = clf.predict(cross_validation_data[i])

	correct = 0
	for real, guess in zip(cross_validation_answer[i], perdiction):
		if real == guess:
			correct += 1

	percent_correct.append(correct / articles_per_fold)

	# F1-measure
	f_measure.append(f1_score(cross_validation_answer[i], perdiction, average='weighted'))
	
	count += 1
	file_name = ''
	if reduce_var:
		file_name = str(count) + '_reduced.dot'
	else:
		file_name = str(count) + '.dot'
	with open(file_name, 'w') as f:
		f = export_graphviz(clf, out_file=f, feature_names=words)
	
for i in range(n_folds):
	dot_string = 'dot -Tpdf ' + str(i + 1) + '.dot -o ' + str(i + 1) + '.pdf'
	if reduce_var:
		dot_string = 'dot -Tpdf ' + str(i + 1) + '_reduced.dot -o ' + str(i + 1) + '_reduced.pdf'
	os.system(dot_string)
	dot_string = str(i+1) + '.dot'
	if reduce_var:
		dot_string = str(i+1) + '_reduced.dot'
	os.unlink(dot_string)

accuracy = 0
for i in percent_correct:
	accuracy += i

accuracy /= n_folds

print('Desicion Tree')
print('Percent \t F-measure')
print(round(accuracy*100, 1), '% \t', f_measure)