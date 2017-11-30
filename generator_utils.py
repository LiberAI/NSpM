import collections
import httplib
import json
import logging
import re
import sys
import urllib
import urllib2

ENDPOINT = "http://dbpedia.org/sparql"
GRAPH = "http://dbpedia.org"

def log_statistics ( used_resources ):
    total_number_of_resources = len(used_resources)
    examples_per_instance = collections.Counter()
    for resource in used_resources:
        count = used_resources[resource]
        examples_per_instance.update([count])

    logging.info('{:6d} used resources'.format(total_number_of_resources))
    for usage in examples_per_instance:
        logging.info('{:6d} resources occur \t{:6d} times \t({:6.2f} %) '.format(examples_per_instance[usage], usage, examples_per_instance[usage]*100/total_number_of_resources))


def save_cache ( file, cache ):
    ordered = collections.OrderedDict(cache.most_common())
    with open(file, 'w') as outfile:
        json.dump(ordered, outfile)


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


def strip_brackets(s):
    s = re.sub(r'\([^)]*\)', '', s)
    if "," in s:
        s = s[:s.index(",")]
    return s.strip().lower()


REPLACEMENTS = [
    ['dbo:', 'http://dbpedia.org/ontology/', 'dbo_'],
    ['dbp:', 'http://dbpedia.org/property/', 'dbp_'],
    ['dbr:', 'http://dbpedia.org/resource/', 'dbr_'],
    ['dct:', 'dct_'],
    ['geo:', 'geo_'],
    ['georss:', 'georss_'],
    ['rdf:type', 'rdf_type'],
    ['(', ' par_open '],
    [')', ' par_close '],
    ['{', 'brack_open'],
    ['}', 'brack_close'],
    [' . ', ' sep_dot '],
    ['?', 'var_'],
    ['*', 'wildcard'],
    [' <= ', 'math_leq'],
    [' >= ', 'math_geq'],
    [' < ', 'math_lt'],
    [' > ', 'math_gt']
]


def encode( sparql ):
    encoded_sparql = sparql
    for r in REPLACEMENTS:
        encoding = r[-1]
        for original in r[:-1]:
            encoded_sparql = encoded_sparql.replace(original, encoding)
    return encoded_sparql


def decode ( encoded_sparql ):
    sparql = encoded_sparql
    for r in REPLACEMENTS:
        original = r[0]
        encoding = r[-1]
        sparql = sparql.replace(encoding, original)
        stripped_encoding = str.strip(encoding)
        sparql = sparql.replace(stripped_encoding, original)
    return sparql


def read_template_file(file):
    annotations = list()
    line_number = 1
    with open(file) as f:
        for line in f:
            values = line[:-1].split(';')
            target_classes = [values[0] or None, values[1] or None, values[2] or None]
            question = values[3]
            query = values[4]
            generator_query = values[5]
            id = values[6] if (len(values) >= 7 and values[6]) else line_number
            line_number += 1
            annotation = Annotation(question, query, generator_query, id, target_classes)
            annotations.append(annotation)
    return annotations


class Annotation:
    def __init__(self, question, query, generator_query, id=None, target_classes=None):
        self.question = question
        self.query = query
        self.generator_query = generator_query
        self.id = id
        self.target_classes = target_classes if target_classes != None else []
        self.variables = extract_variables(generator_query)


def extract_variables(query):
    variables = []
    variable_pattern = r'select\s(distinct)?(.*?)where'
    variable_match = re.search(variable_pattern, query, re.IGNORECASE)
    if variable_match:
        letter_pattern = r'\?(\w)'
        variables = re.findall(letter_pattern, variable_match.group((2)))
    return variables


def extract_encoded_entities( encoded_sparql ):
    entity_pattern = r'(dbr_.*?)\s'
    encoded_entities = re.findall(entity_pattern, encoded_sparql)
    return encoded_entities


def extract_entities( sparql ):
    entity_pattern_1 = r'(dbr:.*?)\s'
    entities = re.findall(entity_pattern_1, sparql)
    entity_pattern_2 = r'(http://dbpedia.org/resource/.*?)\s'
    entities += re.findall(entity_pattern_2, sparql)
    return entities
