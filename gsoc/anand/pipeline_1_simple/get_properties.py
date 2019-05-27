import urllib2, urllib, httplib, json, sys, csv, io
import argparse
from bs4 import BeautifulSoup

"""
Section to parse the command line arguments.
"""

parser = argparse.ArgumentParser()
requiredNamed = parser.add_argument_group('Required Arguments');
requiredNamed.add_argument('--url', dest='url', metavar='url', help='Webpage URL: eg-http://mappings.dbpedia.org/server/ontology/classes/Place', required=True)

args = parser.parse_args()
quote_page = args.url
page = urllib2.urlopen(quote_page)
soup = BeautifulSoup(page, "html.parser")

# print type(soup)


fl = 0
for rows in soup.find_all("tr"):
	x = rows.find_all("td")
	if len(x) <= 2:
		fl = 1
		continue	
	if fl == 1:
		fl = 2
		continue

	name = rows.find_all("td")[0].get_text().replace(" (edit)","")
	label = rows.find_all("td")[1].get_text()
	dom = rows.find_all("td")[2].get_text()
	rng = rows.find_all("td")[3].get_text()

	final = name + "," + label + ","  + dom + ","  + rng 
	print final.encode('utf-8')
"""
Name, Label,Domain ,Range
"""
# 	with io.open("test.csv", mode='w', encoding='utf-8') as toWrite:
# 	writer = csv.writer(toWrite)
# 	writer.writerows(props)

