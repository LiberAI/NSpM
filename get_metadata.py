import urllib2, urllib, httplib, json, sys

endpoint = "http://dbpedia.org/sparql"
proxies = {'http': 'http://proxy.iiit.ac.in:8080/', 'https': 'http://proxy.iiit.ac.in:8080/'}
proxy_handler = urllib2.ProxyHandler(proxies)
opener = urllib2.build_opener(proxy_handler)
urllib2.install_opener(opener)

def sparql_query(query):
    param = dict()
    # param["default-graph-uri"] = "graph"
    param["query"] = query
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


q = "SELECT * where { <http://dbpedia.org/resource/Barack_Obama> ?p ?obj . } LIMIT 1"


result = sparql_query(q)
print(result["results"]["bindings"])
