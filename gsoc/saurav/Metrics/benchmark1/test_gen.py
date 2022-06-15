"""
Receives encoded sparql queries, decodes it and then using the 
sparql endpoint fetches the answers so that it can be used to
calculate the f1 score with the qald answers.
"""

from base64 import decode
import sys
import os
import http.client
import json
import logging
import argparse
from tqdm import tqdm
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
sys.path.append(os.getcwd()+'/nspm')
from generator_utils import decode, fix_URI

ENDPOINT = "http://dbpedia.org/sparql"
GRAPH = "http://dbpedia.org"

def query_dbpedia( query ):
    param = dict()
    param["default-graph-uri"] = GRAPH
    param["query"] = query
    param["format"] = "JSON"
    param["CXML_redir_for_subjs"] = "121"
    param["CXML_redir_for_hrefs"] = ""
    param["timeout"] = "600" 
    param["debug"] = "on"
    try:
        resp = urllib.request.urlopen(ENDPOINT + "?" + urllib.parse.urlencode(param))
        j = resp.read()
        resp.close()
    except (urllib.error.HTTPError, http.client.BadStatusLine):
        logging.debug("*** Query error. Empty result set. ***")
        j = '{ "results": { "bindings": [] } }'
    sys.stdout.flush()
    return json.loads(j)

def write_results(data):
    with open("./gsoc/saurav/Metrics/benchmark1/qald_result.json", "w") as w:
        json.dump(data, w)

def fetch_answers(filename):

    finaltrans = []
    file1 = open(filename, 'r', encoding="utf8")
    Lines1 = file1.readlines()
    test_sparql = []
    for i in range(len(Lines1)):
        test_sparql.append(Lines1[i].replace('\n', " "))

    data = []
    test_sparql = test_sparql[:20]
    for i in tqdm(range(len(test_sparql))):
        
        query = test_sparql[i]
        finaltranso = decode(query)
        # finaltranso = fix_URI(finaltranso)
        # print('Decoded translation: {}'.format(finaltranso))
        results = query_dbpedia(finaltranso)
        results = results['results']['bindings']
        res = []
        for result in results:
            val = result['x']['value'].split('/')[-1]
            res.append({"resource": val})

        data.append({"answers": res})
        
    write_results(data)



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument(
        '--sparql_file', dest='sparql_file', metavar='sparql_file', help='sparql file', required=True)
    args = parser.parse_args()
    sparql_file = args.sparql_file

    fetch_answers(sparql_file)