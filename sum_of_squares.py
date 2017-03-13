def SSE(articles, classes, NUM_CLUSTERS):
	clusters = [[] for i in range(NUM_CLUSTERS)]

	for i in range(len(classes)):
		clusters[classes[i]].append(i)

	# Populate average value with Num_clusters empty lists
	average_values = [[] for i in range(NUM_CLUSTERS)]
	# Populate each empty list with the number of words
	for i in range(NUM_CLUSTERS):
		for j in range(len(articles[0])):
			average_values[i].append(0)
	# Average over each cluster and number of words
	for clust in range(len(clusters)):
		for article in clusters[clust]:
			for i in range(len(articles[0])):
				average_values[clust][i] += int(articles[article][i])

	for clust in range(len(average_values)):
		for i in range(len(average_values[clust])):
			average_values[clust][i] /= len(clusters[clust])

	sum_of_squares = []
	for i in range(NUM_CLUSTERS):
		sum_of_squares.append(0)

	length = 0
	for clust in range(len(clusters)):
		for article in clusters[clust]:
			for word, average_word in zip(articles[article], average_values[clust]):
				sum_of_squares[clust] += pow((float(word) - average_word), 2)

	total_sum_of_squares = sum(sum_of_squares)

	return total_sum_of_squares, sum_of_squares