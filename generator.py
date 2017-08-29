#!/usr/bin/env python
"""

Neural SPARQL Machines - Generator module

'SPARQL as a Foreign Language' by Tommaso Soru and Edgard Marx et al., SEMANTiCS 2017
https://w3id.org/neural-sparql-machines/soru-marx-semantics2017.html
https://arxiv.org/abs/1708.07624

"""
import sys
import json
import urllib2, urllib, httplib, json
import random
import re

reload(sys)
sys.setdefaultencoding("utf-8")

ENDPOINT = "http://dbpedia.org/sparql"
GRAPH = "http://dbpedia.org"

TARGET_CLASS = "dbo:Astronaut"

EXAMPLES_PER_TEMPLATE = 300

# ================================================================

def sparql_query(query):
    param = dict()
    param["default-graph-uri"] = GRAPH
    param["query"] = query
    param["format"] = "JSON"
    param["CXML_redir_for_subjs"] = "121"
    param["CXML_redir_for_hrefs"] = ""
    param["timeout"] = "600000" # ten minutes - works with Virtuoso endpoints
    param["debug"] = "on"
    try:
        resp = urllib2.urlopen(ENDPOINT + "?" + urllib.urlencode(param))
        j = resp.read()
        resp.close()
    except (urllib2.HTTPError, httplib.BadStatusLine):
        print "*** Query error. Empty result set. ***"
        j = '{ "results": { "bindings": [] } }'
    sys.stdout.flush()
    return json.loads(j)

def extract(data):
    res = list()
    for result in data:
        res.append(result)
    print res
    
    if len(res) == 0:
        return None
    
    indx = set()
    while True:
        indx.add(int(random.random() * len(res)))
        print indx
        if len(indx) == EXAMPLES_PER_TEMPLATE or len(indx) == len(res):
            break
    
    xy = list()
    for i in indx:
        result = res[i]
        x = result["x"]["value"]
        lx = result["lx"]["value"]
        print "x = {} -> {}".format(x, lx)
        try:
            y = result["y"]["value"]
            ly = result["ly"]["value"]
            print "y = {} -> {}".format(y, ly)
        except KeyError:
            y = None
            ly = None
        xy.append((x,lx,y,ly))
        
    return xy
    
def strip_brackets(s):
    # strip off brackets
    s = re.sub(r'\([^)]*\)', '', s)
    # strip off everything after comma
    if "," in s:
        s = s[:s.index(",")]
    # strip off spaces and make lowercase
    return s.strip().lower()
    
def replacements(s):
    repl = [
        ('http://dbpedia.org/ontology/', 'dbo_'),
        ('http://dbpedia.org/property/', 'dbp_'),
        ('http://dbpedia.org/resource/', 'dbr_'),
        ('dbr:', 'dbr_'),
        ('dbo:', 'dbo_'),
        ('dbp:', 'dbp_'),
        ('dct:', 'dct_'),
        ('geo:', 'geo_'),
        ('georss:', 'georss_'),
        ('rdf:type', 'rdf_type'),
        ('(', ' par_open '),
        (')', ' par_close '),
        ('{', 'brack_open'),
        ('}', 'brack_close'),
        (' . ', ' sep_dot '),
        ('?', 'var_'),
        ('*', 'wildcard'),
        (' <= ', 'math_leq'),
        (' >= ', 'math_geq'),
        (' < ', 'math_lt'),
        (' > ', 'math_gt'),
    ]
    for r in repl:
        s = s.replace(r[0], r[1])
    return s
    
# ================================================================

annot = list()
with open('annotations_astronaut.tsv') as f:    
    for line in f:
        annot.append(tuple(line[:-1].split('\t')))

cache = dict()
with open('data_astronaut_300.en', 'w') as f1:
    with open('data_astronaut_300.sparql', 'w') as f2:
        for a in annot:
            if a[2] in cache:
                results = cache[a[2]]
            else:
                q = a[2].replace(" C ", " {} ".format(TARGET_CLASS)).replace(" where { ", " (str(?labx) as ?lx) where { ?x rdfs:label ?labx . FILTER(lang(?labx) = 'en') . ")
                if "?y" in q:
                    q = q.replace(" where { ", " (str(?laby) as ?ly) where { ?y rdfs:label ?laby . FILTER(lang(?laby) = 'en') . ")
                print q
                results = sparql_query(q)
                cache[a[2]] = results
            print "ans length = {}".format(len(str(results)))
    
            xy_array = extract(results["results"]["bindings"])
            if xy_array is None:
                print "\nNO DATA FOR '{}'".format(a[0])
                continue
            
            for xy in xy_array:
                inp = a[0].replace("<A>", strip_brackets(xy[1]))
                outp = a[1].replace("<A>", xy[0])
                if "<B>" in inp:
                    if xy[3] is not None:
                        inp = inp.replace("<B>", strip_brackets(xy[3]))
                    else:
                        continue
                if "<B>" in outp:
                    if xy[2] is not None:
                        outp = outp.replace("<B>", xy[2])
                    else:
                        continue
                outp = replacements(outp)
    
                print "\n{}\n{}\n{}".format(xy, inp, outp)
                f1.write("{}\n".format(inp))
                f2.write("{}\n".format(outp))
