import urllib2, urllib, httplib, json, sys

endpoint = "http://dbpedia.org/sparql"
proxies = {'http': 'http://proxy.iiit.ac.in:8080/', 'https': 'http://proxy.iiit.ac.in:8080/'}
graph = "http://dbpedia.org"

proxy_handler = urllib2.ProxyHandler(proxies)
opener = urllib2.build_opener(proxy_handler)
urllib2.install_opener(opener)

Q = dict()
Q["sorted"] = "SELECT DISTINCT ?p (COUNT(*) AS ?c) WHERE { ?s ?p ?o . ?s a mydbo . } GROUP BY ?p ORDER BY DESC(?c)"
Q["prop-metadata"] = "SELECT DISTINCT ?p ?dom ?rng STR(?lab) WHERE { ?s ?p ?o . ?s a mydbo . ?p a rdf:Property . ?p rdfs:label ?lab . OPTIONAL { ?p rdfs:domain ?dom } . OPTIONAL { ?p rdfs:range ?rng } . FILTER(lang(?lab) = 'en') . } "
Q["count"] = "SELECT DISTINCT (COUNT(*) AS ?c) WHERE { ?s ?p ?o . ?s a mydbo . } GROUP BY ?p "

def create_query(curr_class, type, offset=None, limit=None):
		
	query = Q[type]
	if type!="count":
		if offset is not None:
			query += " OFFSET " + str(offset)
		if limit is not None:
			query += " LIMIT " + str(limit)
	query = query.replace("mydbo","dbo:"+ curr_class)
	print query
	return query

def sparql_query(query):
    param = dict()
    param["default-graph-uri"] = graph
    param["query"] = query 
    print query
    # print param["query"]
    param["format"] = "JSON"
    param["CXML_redir_for_subjs"] = "121"
    param["CXML_redir_for_hrefs"] = ""
    param["timeout"] = "600000" # ten minutes - works with Virtuoso endpoints
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
TOTAL = 


for i in 

q = create_query("Place","count",0,100)

result = sparql_query(q)
print(result["results"]["bindings"])

