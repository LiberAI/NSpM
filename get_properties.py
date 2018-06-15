import urllib2, urllib, httplib, json, sys, csv, io
from bs4 import BeautifulSoup

quote_page = "http://mappings.dbpedia.org/server/ontology/classes/Place"
page = urllib2.urlopen(quote_page)

soup = BeautifulSoup(page, "html.parser")
# print type(soup)

props = []
final = ""
cnt = 0
for rows in soup.find_all("tr"):
	cnt += 1
	if cnt<=18: continue
	name = rows.find_all("td")[0].get_text().replace(" (edit)","")
	label = rows.find_all("td")[1].get_text()
	dom = rows.find_all("td")[2].get_text()
	rng = rows.find_all("td")[3].get_text()

	final = name + "," + label + ","  + dom + ","  + rng 
	print final.encode('utf-8')

# with io.open("test.csv", mode='w', encoding='utf-8') as toWrite:
# 	writer = csv.writer(toWrite)
# 	writer.writerows(props)

