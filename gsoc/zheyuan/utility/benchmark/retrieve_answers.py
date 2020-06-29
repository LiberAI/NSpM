import argparse
import os

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def read_sparqls():
    os.system("pwd")
    sparqls = []
    file_path = "../gsoc/zheyuan/utility/benchmark/output_decoded.txt"
    with open(file_path, 'r') as lines:
        for line in lines:
            sparqls.append(line)
    return sparqls

def retrieve(query):
    try:  # python3
        query = urllib.parse.quote_plus(query)
    except:  # python2
        query = urllib.quote_plus(query)
    url = "https://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=" + query + "&format=text%2Fhtml&CXML_redir_for_subjs=121&CXML_redir_for_hrefs=&timeout=30000&debug=on&run=+Run+Query+"
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    total = len(soup.find_all("tr"))
    answers = []

    for rows in (soup.find_all("tr")):
        for td in rows.find_all("a"):
            for a in td:
                answer_dict = {
                    "head" : {
                      "vars" : [ "uri" ]
                    },"results": {
                        "bindings": [{
                            "uri": {
                                "type": "uri",
                                "value": a
                            }
                        }]
                    }
                }
                answers.append(answer_dict)
        for td in rows.find_all("pre"):
            for pre in td:
                # Eliminate the answer if it is longer than 50(not a URI nor a simple literal)
                if len(pre) <= 50:
                    answer_dict = {
                        "results": {
                            "head": {
                                "vars": ["string"]
                            },
                            "bindings": [{
                                "string": {
                                    "type": "literal",
                                    "value": pre
                                }
                            }]
                        }
                    }
                    answers.append(answer_dict)
    return answers


if __name__ == "__main__":
    """
    Section to parse the command line arguments.
    """
    # parser = argparse.ArgumentParser()
    # requiredNamed = parser.add_argument_group('Required Arguments')
    #
    # requiredNamed.add_argument('--query', dest='query', metavar='query',
    #                            help='query of SPARQL', required=True)
    # args = parser.parse_args()
    # query = args.query
    answer_groups = []
    i = 1
    with open("./output_decoded.txt", 'r') as lines:
         for line in lines:
             i+=1
             try:
                 answer_group = retrieve(line)
             except:
                 answer_group=[]
             answer_groups.append(answer_group)

    print(len(answer_groups), answer_groups)


    pass