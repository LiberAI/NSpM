"""
Parses the qald-9-train-multilingual.json file and generates updated-qald-9-train-multilingual.json file
"""

from base64 import decode
import sys
import os
import http.client
import json
import logging
import argparse
from torch import feature_alpha_dropout
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

def fetch_answers(sparql, type):

    query = sparql
    results = query_dbpedia(query)
    res = []
    if type == 'boolean':
        results = results['boolean']
        return results
    else:
        results = results['results']['bindings']
        res = []
        for result in results:
            res.append(result)

    return res

def update_qald(qald_file):

    with open(qald_file, encoding='utf-8') as f:
        data = json.load(f)
    data  = data['questions']
    sparql = []
    update_data = []
    for sub_data in tqdm(data):

        if sub_data['answertype'] == 'boolean':
            # Fetching sparql query
            sparql = sub_data['query']['sparql']
            answers_data = fetch_answers(sparql, 'boolean')
            # Updating answers
            sub_data['answers'][0]['boolean'] = answers_data
            update_data.append(sub_data)
        else:
            # Fetching sparql query
            sparql = sub_data['query']['sparql']
            answers_data = fetch_answers(sparql, None)
            # Updating answers
            sub_data['answers'][0]['results']['bindings'] = answers_data
            update_data.append(sub_data)
    
    final_data = { 
        "dataset" : {
        "id" : "qald-9-train-multilingual"
        }
    }
    final_data['questions'] = update_data
    return final_data

def write_results(data):
    with open("gsoc/saurav/Metrics/benchmark1/updated-qald-9-train-multilingual.json", "w") as w:
        json.dump(data, w, ensure_ascii = False)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument(
        '--qald_file', dest='qald_file', metavar='qald_file', help='qald file', required=True)
    args = parser.parse_args()
    qald_file = args.qald_file

    final_data = update_qald(qald_file)
    write_results(final_data)
