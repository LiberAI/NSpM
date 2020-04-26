import urllib2, urllib, httplib, json, sys
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')

endpoint = "http://dbpedia.org/sparql"

proxies = {'http': 'http://proxy.iiit.ac.in:8080/', 'https': 'http://proxy.iiit.ac.in:8080/'}
graph = "http://dbpedia.org"

proxy_handler = urllib2.ProxyHandler(proxies)
opener = urllib2.build_opener(proxy_handler)
urllib2.install_opener(opener)

Q = dict()
Q["sorted"] = "SELECT DISTINCT ?p (COUNT(*) AS ?c) WHERE { ?s ?p ?o . ?s a mydbo . } GROUP BY ?p ORDER BY DESC(?c)"
Q["prop-metadata-dom"] = "SELECT DISTINCT ?p ?lab ?dom WHERE { ?s ?p ?o . ?s a mydbo . ?p a rdf:Property . ?p rdfs:label ?lab . OPTIONAL { ?p rdfs:domain ?dom } . FILTER(lang(?lab) = 'en') . } "
Q["prop-metadata-rng"] = "SELECT DISTINCT ?p ?lab ?rng WHERE { ?s ?p ?o . ?s a mydbo . ?p a rdf:Property . ?p rdfs:label ?lab . OPTIONAL { ?p rdfs:range ?rng } . FILTER(lang(?lab) = 'en') .  } "
Q["count"] = "SELECT DISTINCT (COUNT(*) AS ?c) WHERE { ?s ?p ?o . ?s a mydbo . ?p a rdf:Property . } GROUP BY ?p "

def create_query(curr_class, type, offset=None, limit=None):
		
	query = Q[type]
	if type!="count":
		if offset is not None:
			query += " OFFSET " + str(offset)
		if limit is not None:
			query += " LIMIT " + str(limit)
	query = query.replace("mydbo", "dbo:"+ curr_class)
	print query
	return query

def sparql_query(query):
    param = dict()
    # param["default-graph-uri"] = graph
    param["query"] = query 
    print query
    # print param["query"]
    param["format"] = "JSON"
    param["CXML_redir_for_subjs"] = "121"
    param["CXML_redir_for_hrefs"] = ""
    param["timeout"] = "36000" # ten minutes - works with Virtuoso endpoints
    param["debug"] = "on"
    try:
        resp = urllib2.urlopen(endpoint + "?" + urllib.urlencode(param))
        print(resp)
        j = resp.read()
        resp.close()
    except (urllib2.HTTPError, httplib.BadStatusLine):
		print("*** Query error. Empty result set. ***")
		j = '{ "results": { "bindings": [] } }'
    sys.stdout.flush()
    return json.loads(j)

## MAIN ## 

q = create_query("Place","prop-metadata-dom", 0, 10)
result = sparql_query(q)

total_prop = len(result["results"]["bindings"])
print total_prop
print (result["results"]["bindings"])
# with open("test.txt", "a") as myfile:
    # myfile.write(json.dumps(result["results"]["bindings"]))

# TOTAL = 


# for i in 
# final = dict()
# final["dom"], final["rng"] = [], []
# # for i in
# i,total_prop = 0,0
# limit = 10000
# while 1:
#     if len(result["results"]["bindings"]) == 0:
#         break;
#     final["dom"].append(result["results"]["bindings"])
#     i += 1
#     # if i == 2:
#     #     break;

# i = 0
# limit = 10000
# while 1:
#     q = create_query("Place","prop-metadata-rng", i * limit, limit)
#     result = sparql_query(q)
#     if len(result["results"]["bindings"]) == 0:
#         break;
#     final["rng"].append(result["results"]["bindings"])
#     i += 1
#     # if i==2:
#     #     break;

# # print final["dom"] 
# # print final["rng"]

# Output = dict()
# cnt, cnt2 = 0 ,0 
# for i in final["dom"]:
#     for j in i:
#         cnt += 1
#         print "dom for prop", str(j["p"]["value"])
#         curr = dict()
#         # curr[]
#         # print "i is", i
#         # curr["prop"] = i[0]["p"]["value"]
#         curr["label"] = j["lab"]["value"]
#         try:
#             curr["domain"] = j["dom"]["value"]
#         except:
#             curr["domain"] = "NONE"
#         Output[str(j["p"]["value"])] = curr


# for i in final["rng"]:
#     for j in i:
#     # print "i is", i
#         cnt2 += 1

#         print "rng for prop", str(j["p"]["value"])

#         try:
#             Output[str(j["p"]["value"])]["range"] = j["rng"]["value"]
#         except:
#             try:
#                 Output[str(j["p"]["value"])]["range"] = "NONE"
#             except:
#                 print "No such prop: ", str(j["p"]["value"])
# print Output
#     # curr["label"] = final["p"]["value"]
# print "total: ", total_prop, cnt, cnt2
# with open('metadata_place.txt', 'w') as file:
#      file.write(json.dumps(Output))

