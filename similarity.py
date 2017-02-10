import math
import csv 		# Convert to spreadsheet format


with open("data.csv", 'r') as csvfile:
	# Read each row in csv file
	rows = csvfile.readlines()

	# article name name
	article = []

	# Split each row based on tabs (to form columns)
	for i in range(len(rows)):
		rows[i] = rows[i].split('\t')
		# Get article name
		article.append(rows[i][0])

	# Take out 'SITE'
	article = article[1:]

	rows[0][-1] = rows[0][-1]

	# Total number of words, plus 2 (for SITE and WORD_COUNT)
	number_of_words = len(rows[0]) 

	# Get word count per columns
	total_column_word_count = [0] * number_of_words

	for row in range(1, len(rows)):
		for column in range(1, number_of_words):
			rows[row][column] = int(rows[row][column]) 	# Convert each string number to an actual number
			total_column_word_count[column] += rows[row][column]

	### Euclidean Distance Similarity ###
	euclidean_distance_between_pairs = []

	for row in range(1, len(rows)):
		distance_between_each_pair = []
		for pair in range(1, len(rows)):
			# Compute euclidean distance
			distance_between_each_pair.append(math.sqrt(sum((rows[row][column] - rows[pair][column]) ** 2 for column in range(2, number_of_words))))

		euclidean_distance_between_pairs.append(distance_between_each_pair)

	## Convert to similarity ##
	# Find maximum
	maximum = 0
	for row in euclidean_distance_between_pairs:
		for column in row:
			if maximum < column:
				maximum = column
	# Take 1 - (distance / max) to standardize it
	for row in range(len(euclidean_distance_between_pairs)):
		for column in range(len(euclidean_distance_between_pairs[row])):
			euclidean_distance_between_pairs[row][column] = 1 - (euclidean_distance_between_pairs[row][column] / maximum)

	euclidean_distance_similarity = euclidean_distance_between_pairs
	
	print(euclidean_distance_between_pairs)

	### Cosine Similarity ###
	cosine_similarity = []

	for row in range(1, len(rows)):
		distance_between_each_pair = []
		for pair in range(1, len(rows)):
			# Compute cosine_similarity
			d1_times_d2 = 0
			distance_d1 = 0
			distance_d2 = 0

			for column in range(2, number_of_words):
				d1_times_d2 += rows[row][column] * rows[pair][column] 
				distance_d1 += rows[row][column] ** 2
				distance_d2 += rows[pair][column] ** 2

			distance_d1 = math.sqrt(distance_d1)
			distance_d2 = math.sqrt(distance_d2)

			cosine = d1_times_d2 / (distance_d1 * distance_d2)
			if cosine > 1.0:
				cosine = 1.0

			distance_between_each_pair.append(cosine)

		cosine_similarity.append(distance_between_each_pair)

	print(cosine_similarity)

	### Jaccard Similarity (binary) ###

	jaccard_similarity = []

	for row in range(1, len(rows)):
		distance_between_each_pair = []
		for pair in range(1, len(rows)):
			# Compute Jaccard
			intersect = 0
			union = 0
			for column in range(2, number_of_words):
				if ((rows[row][column] > 0) and (rows[pair][column] > 0)):
					intersect += 1
					union += 1
				elif rows[row][column] > 0 or rows[pair][column] > 0:
					union += 1
			# Jaccard = union / intersect
			if union == 0:
				union = 1
			distance_between_each_pair.append(intersect / union)

		jaccard_similarity.append(distance_between_each_pair)

	print(jaccard_similarity)

	print(article)

	# Create csv document for Euclidean distance
	with open("euclidean.csv", 'w') as csvfile:
		# csv formatting
		writer = csv.writer(csvfile, delimiter='\t',quoting=csv.QUOTE_MINIMAL)

		# Write article names on top
		writer.writerow([' '] + article)

		# For each article:
		print(len(article))
		for art in range(len(article)):
			print(art)
			writer.writerow([article[art]] + euclidean_distance_between_pairs[art])

	# Create csv document for Cosine distance
	with open("cosine.csv", 'w') as csvfile:
		# csv formatting
		writer = csv.writer(csvfile, delimiter='\t',quoting=csv.QUOTE_MINIMAL)

		# Write article names on top
		writer.writerow([' '] + article)

		# For each article:
		print(len(article))
		for art in range(len(article)):
			print(art)
			writer.writerow([article[art]] + cosine_similarity[art])

	# Create csv document for Jaccard Distance
	with open("jaccard.csv", 'w') as csvfile:
		# csv formatting
		writer = csv.writer(csvfile, delimiter='\t',quoting=csv.QUOTE_MINIMAL)

		# Write article names on top
		writer.writerow([' '] + article)

		# For each article:
		print(len(article))
		for art in range(len(article)):
			print(art)
			writer.writerow([article[art]] + jaccard_similarity[art])

		'''
		# For each word
		for site, word_count in zip(web_to_words, total_words):
			# List of every word on the site
			words = web_to_words[site]

			# List of the frequency of all of the words in the same order as all_words is in
			word_frequency = []

			# For every word
			for word in all_words:
				# If in site, append frequency, if not, append a 0
				if word in words:
					word_frequency.append(words[word])
				else:
					word_frequency.append(0)

			test = [site] + [word_count] + word_frequency
			# Write site title and word frequency as a row in csv
			writer.writerow(test)
		'''


