'''
__author__: 	Dalton Cole
__description__:This script counts the frequency of words in a CNN article. It does this
					by using the URLs contained in website_list. It then parses the 
					HTML of every webpage extracting the data for the article in the
					"zn-body_paragraph" class div. If this div is not present, this
					script does not work. The data is then saved in csv format under
					data.csv
'''

from urllib.request import urlopen	# Get url
from bs4 import BeautifulSoup		# Parse HTML
import re 							# Take out punctuation
import csv 							# Convert to spreadsheet format
from nltk.corpus import stopwords	# Get rid of generic words

# max articles
max_articles = 100

# Dictionary of article titles to the words and frequency of words in them
web_to_words = {}
# List of all of the words
all_words = []

# String of websites
websites = ""

# Generic word list
generic_words = set(stopwords.words('english'))

# Read in string of websites form website_list
with open('website_list', 'r') as f:
	websites = f.readlines()

site_list = []

# For each website in website_list
for site in websites:
	print(site)
	# Dictionary mapping words to frequency
	word_list = {}

	# Word count for article
	word_count = 0

	# Get HTML
	url = None
	while url == None:
		try:
			url = urlopen(site, timeout=3000)
		except:
			print('Failed in urlopen, trying again')

	r = url.read()
	html = r.decode("utf8")
	url.close()

	# Parse HTML
	soup = BeautifulSoup(html, "lxml")

	# Get title of article
	title = soup.title.string

	# Get every word in article
	strings = ""
	for div in soup.findAll("div", { "class" : "zn-body__paragraph" }):
		strings += div.text + ' '

	if strings == "":
		for p in soup.findAll('p'):
			strings += p.text + ' '

	if strings is "":
		print("NO zn-body__paragraph DIV CLASS or p, CHOOSE DIFFERENT ARTICLE, PERFERABLY IN CNN POLITICS")
		print(site)
		#raise SystemExit(0)

	# Get rid of puntuation
	strings = (re.sub(r'([^\s\w]|_)+', '', strings)).lower()

	# Only accept articles with more than 100 words
	if strings.count(' ') < 150:
		continue

	# Get rid of generic words
	meaningful_words = filter(lambda w: not w in generic_words, strings.split())

	# For every word in the article
	for word in meaningful_words:
		word = word.lower()
		word_count += 1
		# Increase word frequency by 1
		if word in word_list:
			word_list[word] += 1
		else:
			word_list[word] = 1

		# Add word to complete word list
		if word not in all_words:
			all_words.append(word)

	# Add title and word/frequency to dictionary
	web_to_words[title] = word_list

	num_end = False
	a_type = ''
	for slash in site.split('/'):
		if slash.isdigit():
			num_end = True
		elif num_end:
			a_type = slash
			break

	site_list.append(site)

	# Add title and word/frequency to dictionary
	web_to_words[title] = (word_list, word_count, a_type)

	if len(site_list) >= max_articles:
		break

# Make list of websites included
with open("used_site_list.txt", 'w') as f:
	for i in site_list:
		f.write(i)

# Create csv document
with open("data.csv", 'w') as csvfile:
	# csv formatting
	writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	# Write all of the words to the top row
	space_with_all_words = ['SITE', 'TYPE', 'WORD COUNT'] + all_words
	writer.writerow(space_with_all_words)

	'''
	for a in web_to_words.keys():
		print(a)
	'''

	# For each word
	for site in web_to_words:
		# List of every word on the site
		words = web_to_words[site]

		article_t = words[2]
		word_count = words[1]
		words = words[0]

		# List of the frequency of all of the words in the same order as all_words is in
		word_frequency = []

		# For every word
		for word in all_words:
			# If in site, append frequency, if not, append a 0
			if word in words:
				word_frequency.append(words[word])
			else:
				word_frequency.append(0)

		test = [site] + [article_t] + [word_count] +  word_frequency
		# Write site title and word frequency as a row in csv
		writer.writerow(test)