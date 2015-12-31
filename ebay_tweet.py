from twython import Twython
from twython import TwythonRateLimitError, TwythonError
import json
from oauth2client.client import SignedJwtAssertionCredentials
import gspread
import re

consumer_key = '1GjfZ4mXMhJ3cEjtsPRcOD91n'
consumer_secret = 'zJNo9oSTqg0oOUd9aVJBUJMZaDM3YFIxa2A8B4P0ifGT68qgUL'
access_token = '3426802858-yFOOhNRddjWsl1qW4D1Qqin4J7nUydPGv9tgpTg'
access_secret = '4RCZ15tfrwTj8YBS7e4DKX6vnUvb0EsRClzvstkht20Ru'

twitter = Twython(consumer_key, consumer_secret, access_token, access_secret)

def post_tweet(tweet):
	try:
		twitter.update_status(status=tweet)
	except TwythonError:
		print 'Twython error, probably already tweeted...'
	except TwythonRateLimitError:
		print TwythonRateLimitError



def tweet_match(query):
	json_key = json.load(open('ebay-c386c1f03285.json'))
	scope = ['https://spreadsheets.google.com/feeds']
	credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
	gc = gspread.authorize(credentials)
	sh = gc.open("ebay")
	worksheet = sh.get_worksheet(0)
	cell_list = worksheet.range('A1:A200')
	print 'looking matches to tweet'
	for cell in cell_list:

		if len(cell.value) > 1:
			val = cell.value.encode('utf-8')
			# m = re.search(r'\b{}\b'.format(query), val, re.IGNORECASE)

			if query.lower() in val.lower():
				status = '{} {}'.format('@johnsimmons517', val)
				if len(status) <= 140:
					print 'Potential status: {}'.format(status)
					post_tweet(status)
				elif len(status) >= 141:
					status = status[:140]
					print 'Potential status: {}'.format(status)
					post_tweet(status)
				else:
					print 'something wrong with tweet'
		else:
			return
