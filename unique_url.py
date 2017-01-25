websites = []
with open('website_list', 'r') as f:
	url = f.readlines()
	for u in url:
		websites.append(u)


unique_websites = sorted(set(websites))

if(len(websites) != len(unique_websites)):
	with open('website_list', 'w') as f:
		for url in unique_websites:
			f.write(url)

