from bs4 import BeautifulSoup
from oauth2client.client import SignedJwtAssertionCredentials
import datetime
import gspread
import json
import mechanize
import re
import sched
import time
from ebay_tweet import *
import urllib2

url = 'http://www.ebay.com/sch/Records-/176985/i.html'

queries = sorted([line.rstrip('\n') for line in open('q.txt')])

master_list = []
master_list_flat = []

# Set up mechanization
br = mechanize.Browser()
br.set_handle_robots(False)

# Listings and posting
def clear_values():
	json_key = json.load(open('ebay-c386c1f03285.json'))
	scope = ['https://spreadsheets.google.com/feeds']
	credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
	gc = gspread.authorize(credentials)
	sh = gc.open("ebay")
	worksheet = sh.get_worksheet(0)
	cell_list = worksheet.range('A1:C200')

	for cell in cell_list:
	    cell.value = ' '
	# Update in batch
	worksheet.update_cells(cell_list)
def search_count(html):
	for num in html:
		search_num = int(re.search('\d+', str(num)).group(0))
	return search_num
def price(html):
	price_num = re.search('\d+\.\d{2}', html).group(0)
	return price_num
def search_and_sort(query):
	while True:
		try:
			br.open(url).read()
			# Search Box
			br.form = list(br.forms())[0]

			# Initial search
			for control in br.form.controls:
			    if control.type == 'text':
			    	control.value = query
			
			results = br.submit().read()

			soup = BeautifulSoup(results, 'html5lib')
			listing_count_html = soup.find_all('span', {'class': 'listingscnt'})
			price_html = soup.find_all('span', {'class':'bold'})
			records_check = soup.find_all('div', {'class':'cat-st'})

			if records_check:
				listings = []
				count = 0
				for link in br.links():
					try:
						if '[IMG]' not in link.text and 'vip' in link.attrs[1][1]:
							listings.append((link.text, link.url, price(str(price_html[count]))))
							count += 1
					except:
						continue
				del listings[search_count(listing_count_html):]		
				return listings
			else:
				pass
		except:
			continue
		break
def gen_master_list(queries):
	global master_list
	for q in queries:
		print q
		if search_and_sort(q):
			master_list.append(search_and_sort(q))
		else:
			continue
	return master_list
def post_listings():
	global master_list_flat
	json_key = json.load(open('ebay-c386c1f03285.json'))
	scope = ['https://spreadsheets.google.com/feeds']
	credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
	gc = gspread.authorize(credentials)
	sh = gc.open("ebay")
	worksheet = sh.get_worksheet(0)

	a_cells = worksheet.range('A1:A{}'.format(len(master_list_flat)))
	b_cells = worksheet.range('B1:B{}'.format(len(master_list_flat)))
	c_cells = worksheet.range('C1:C{}'.format(len(master_list_flat)))

	for idx, cell in enumerate(a_cells, start=1):
		# cell.value = str(idx) + ' : ' + str(cell.col) 
		cell.value = unicode(master_list_flat[idx-1][0], 'utf-8')
	worksheet.update_cells(a_cells)

	for idx, cell in enumerate(b_cells, start=1):
		# cell.value = str(idx) + ' : ' + str(cell.col) 
		cell.value = unicode(master_list_flat[idx-1][2], 'utf-8')
	worksheet.update_cells(b_cells)

	for idx, cell in enumerate(c_cells, start=1):
		# cell.value = str(idx) + ' : ' + str(cell.col) 
		cell.value = master_list_flat[idx-1][1]
	worksheet.update_cells(c_cells)

	worksheet.update_cell(len(master_list_flat)+2, 1, datetime.datetime.now().strftime("%r %m-%d-%Y"))



def executeSomething():

	#code here
	global queries
	global master_list_flat
	global master_list
	print 'searching {}'.format(datetime.datetime.now().strftime("%r %m-%d-%Y"))
	gen_master_list(queries)	
	print 'generated master list'
	# Flatten lists
	print 'flattening master list'
	master_list[:] = [item for item in master_list if item != None] #typeerror fix?
	master_list_flat = [item for sublist in master_list for item in sublist]
	print 'master list flattened'
	clear_values()
	print 'values cleared'
	post_listings()
	print 'posted {}'.format(datetime.datetime.now().strftime("%r %m-%d-%Y"))

	# erase lists
	del master_list[:]
	del master_list_flat[:]
	print 'lists erased'

	# print 'searching for matches to tweet'
	tweet_match('integrity')
	tweet_match('thou')
	post_tweet('New record list posted')

	print 'Done. Next search in 2 hours'
	time.sleep(7200)

while True:
    executeSomething()
