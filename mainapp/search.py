from twython import Twython

def search_general(twitter, keyword = '', mention_name = ['@kaflesudip'], hashtags = [], location = ''):
	query = keyword
	for each in mention_name:
		query = query + ' ' + each + ' AND '
	for each in hashtags:
		query = query + ' ' + each
	print query
	if location:
		search_results = twitter.search(q=query, geocode = location, result_type = "recent", count = 20)
	else:
		search_results = twitter.search(q=query, result_type = "recent", count = 20)
	return search_results