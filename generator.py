#!/usr/bin/env python
"""

Neural SPARQL Machines - Generator module

'SPARQL as a Foreign Language' by Tommaso Soru and Edgard Marx et al., SEMANTiCS 2017
https://w3id.org/neural-sparql-machines/soru-marx-semantics2017.html
https://arxiv.org/abs/1708.07624

"""
import argparse
import logging
import os
import sys
import urllib2, urllib, httplib, json
import random
import re

logging.basicConfig(filename='generator.log', level=logging.DEBUG)
ENDPOINT = "http://dbpedia.org/sparql"
GRAPH = "http://dbpedia.org"


def query_dbpedia( query ):
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
        logging.debug("*** Query error. Empty result set. ***")
        j = '{ "results": { "bindings": [] } }'
    sys.stdout.flush()
    return json.loads(j)

def extract(data):
    EXAMPLES_PER_TEMPLATE = 300
    res = list()
    for result in data:
        res.append(result)
    logging.debug(res)
    
    if len(res) == 0:
        return None
    
    indexes = set()

    if len(res) < EXAMPLES_PER_TEMPLATE:
        index_range = range(len(res))
        indexes = set(random.shuffle(index_range))
    else:
        while len(indexes) < EXAMPLES_PER_TEMPLATE:
            indexes.add(int(random.random() * len(res)))

    logging.debug(indexes)

    uri_label_pairs = list()
    for index in indexes:
        result = res[index]
        x = result["x"]["value"]
        lx = result["lx"]["value"]
        logging.debug("x = {} -> {}".format(x, lx))
        if "y" in result:
            y = result["y"]["value"]
            ly = result["ly"]["value"]
            logging.debug("y = {} -> {}".format(y, ly))
        else:
            y = None
            ly = None
        uri_label_pairs.append((x,lx,y,ly))
        
    return uri_label_pairs
    
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

class Annotation:
    def __init__(self, question, query, generator_query, id=None, target_classes=None):
        self.question = question
        self.query = query
        self.generator_query = generator_query
        self.id = id
        self.target_classes = target_classes if target_classes != None else []

def read_template_file(file):
    annotations = list()
    line_number = 1
    with open(file) as f:
        for line in f:
            values = line[:-1].split(';')
            target_classes = [values[0] or None, values[1] or None]
            question = values[2]
            query = values[3]
            generator_query = values[4]
            id = values[5] if len(values) >= 6 else line_number
            line_number += 1
            annotation = Annotation(question, query, generator_query, id, target_classes)
            annotations.append(annotation)
    return annotations

def build_dataset_pair(binding, template):
    english_template_question = getattr(template, 'question')
    sparql_template_query = getattr(template, 'query')
    uri_a = binding[0]
    label_a = binding[1]
    english = english_template_question.replace("<A>", strip_brackets(label_a))
    sparql = sparql_template_query.replace("<A>", uri_a)
    if "<B>" in english:
        label_b = binding[3]
        if label_b is not None:
            english = english.replace("<B>", strip_brackets(label_b))
        else:
            return None
    if "<B>" in sparql:
        uri_b = binding[2]
        if uri_b is not None:
            sparql = sparql.replace("<B>", uri_b)
        else:
            return None
    sparql = replacements(sparql)
    dataset_pair = {'english': english, 'sparql': sparql}
    return dataset_pair


def extract_variables(query):
    variables = []
    variable_pattern = variable_pattern = r'select.*?\?([a-zA-Z]).*?(\?([a-zA-Z]).*?)?where'
    variable_match = re.search(variable_pattern, query, re.IGNORECASE)
    groups = variable_match.groups()
    variable_group_indexes = [0, 2]
    for i in variable_group_indexes:
        if groups[i]:
            variables.append(groups[i])
    return variables


def generate_dataset(templates, output_dir):
    cache = dict()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_dir + '/data_300.en', 'w') as english_questions:
        with open(output_dir + '/data_300.sparql', 'w') as sparql_queries:
            for template in templates:
                results = get_results_of_generator_query(cache, template)
                logging.debug("ans length = {}".format(len(str(results))))

                bindings = extract(results["results"]["bindings"])
                if bindings is None:
                    logging.debug("\nNO DATA FOR '{}'".format(getattr(template, 'id')))
                    continue

                for binding in bindings:
                    dataset_pair = build_dataset_pair(binding, template)

                    if (dataset_pair):
                        logging.debug("\n{}\n{}\n{}".format(binding, dataset_pair['english'], dataset_pair['sparql']))
                        english_questions.write("{}\n".format(dataset_pair['english']))
                        sparql_queries.write("{}\n".format(dataset_pair['sparql']))


def get_results_of_generator_query( cache, template ):
    generator_query = getattr(template, 'generator_query')

    if generator_query in cache:
        results = cache[generator_query]
    else:
        query = prepare_generator_query(template)
        logging.debug(query)
        results = query_dbpedia(query)
        cache[generator_query] = results
    return results


def prepare_generator_query( template ):
    query = getattr(template, 'generator_query')
    target_classes = getattr(template, 'target_classes')
    variables = extract_variables(query)

    add_requirement = lambda query, where_replacement: query.replace(" where { ", where_replacement)
    LABEL_REPLACEMENT = " (str(?lab%(variable)s) as ?l%(variable)s) where { ?%(variable)s rdfs:label ?lab%(variable)s . FILTER(lang(?lab%(variable)s) = 'en') . "
    CLASS_REPLACEMENT = " where { ?%(variable)s a %(class)s . "


    for i, variable in enumerate(variables):
        query = add_requirement(query, LABEL_REPLACEMENT % {'variable': variable})
        variable_has_a_type = len(target_classes) > i and target_classes[i]
        if variable_has_a_type:
            query = add_requirement(query, CLASS_REPLACEMENT % {'variable': variable, 'class': target_classes[i]})

    return query


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('--templates', dest='templates', metavar='templateFile', help='templates', required=True)
    requiredNamed.add_argument('--output', dest='output', metavar='outputDirectory', help='dataset directory', required=True)
    args = parser.parse_args()
    template_file = args.templates
    output_dir = args.output

    reload(sys)
    sys.setdefaultencoding("utf-8")

    templates = read_template_file(template_file)
    generate_dataset(templates, output_dir)
