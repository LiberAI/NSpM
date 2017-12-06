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

def log_statistics( used_resources, special_classes, not_instanced_templates ):
    total_number_of_resources = len(used_resources)
    total_number_of_filled_placeholder_positions = sum(used_resources.values())
    examples_per_instance = collections.Counter()
    for resource in used_resources:
        count = used_resources[resource]
        examples_per_instance.update([count])

    logging.info('{:6d} used resources in {} placeholder positions'.format(total_number_of_resources, total_number_of_filled_placeholder_positions))
    for usage in examples_per_instance:
        logging.info('{:6d} resources occur \t{:6d} times \t({:6.2f} %) '.format(examples_per_instance[usage], usage, examples_per_instance[usage]*100/total_number_of_resources))
    for cl in special_classes:
        logging.info('{} contains: {}'.format(cl, ', '.join(special_classes[cl])))
    logging.info('{:6d} not instanciated templates:'.format(sum(not_instanced_templates.values())))
    for template in not_instanced_templates:
        logging.info('{}'.format(template))


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
    param["timeout"] = "600" # ten minutes - works with Virtuoso endpoints
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
    ['dbc:', 'http://dbpedia.org/resource/Category:', 'dbc_'],
    ['dbr:', 'http://dbpedia.org/resource/', 'dbr_'],
    ['dct:', 'dct_'],
    ['geo:', 'geo_'],
    ['georss:', 'georss_'],
    ['rdf:', 'rdf_'],
    ['rdfs:', 'rdfs_'],
    ['foaf:', 'foaf_'],
    ['skos:', 'skos_'],
    [' ( ', '  par_open  '],
    [' ) ', '  par_close  '],
    ['(', ' attr_open '],
    [')', ' attr_close '],
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


STANDARDS = {
        'dbo_almaMater': ['dbp_almaMater'],
        'dbo_award': ['dbp_awards'],
        'dbo_birthPlace': ['dbp_birthPlace', 'dbp_placeOfBirth'],
        'dbo_deathPlace': ['dbp_deathPlace', 'dbp_placeOfDeath'],
        'dbo_child': ['dbp_children'],
        'dbo_college': ['dbp_college'],
        'dbo_hometown': ['dbp_hometown'],
        'dbo_nationality': ['dbo_stateOfOrigin'],
        'dbo_relative': ['dbp_relatives'],
        'dbo_restingPlace': ['dbp_restingPlaces', 'dbp_placeOfBurial', 'dbo_placeOfBurial', 'dbp_restingplace'],
        'dbo_spouse': ['dbp_spouse'],
        'dbo_partner': ['dbp_partner']
}


def encode( sparql ):
    encoded_sparql = do_replacements(sparql)
    shorter_encoded_sparql = shorten_query(encoded_sparql)
    normalized = normalize_predicates(shorter_encoded_sparql)
    return normalized


def decode ( encoded_sparql ):
    short_sparql = reverse_replacements(encoded_sparql)
    sparql = reverse_shorten_query(short_sparql)
    return sparql


def normalize_predicates( sparql ):
    for standard in STANDARDS:
        for alternative in STANDARDS[standard]:
            sparql = sparql.replace(alternative, standard)

    return sparql


def do_replacements( sparql ):
    for r in REPLACEMENTS:
        encoding = r[-1]
        for original in r[:-1]:
            sparql = sparql.replace(original, encoding)
    return sparql


def reverse_replacements( sparql ):
    for r in REPLACEMENTS:
        original = r[0]
        encoding = r[-1]
        sparql = sparql.replace(encoding, original)
        stripped_encoding = str.strip(encoding)
        sparql = sparql.replace(stripped_encoding, original)
    return sparql


def shorten_query( sparql ):
    sparql = re.sub(r'order by desc\s+....?_open\s+([\S]+)\s+....?_close', '_obd_ \\1', sparql, flags=re.IGNORECASE)
    sparql = re.sub(r'order by asc\s+....?_open\s+([\S]+)\s+....?_close', '_oba_ \\1', sparql, flags=re.IGNORECASE)
    sparql = re.sub(r'order by\s+([\S]+)', '_oba_ \\1', sparql, flags=re.IGNORECASE)
    return sparql


def reverse_shorten_query( sparql ):
    sparql = re.sub(r'_oba_ ([\S]+)', 'order by asc (\\1)', sparql, flags=re.IGNORECASE)
    sparql = re.sub(r'_obd_ ([\S]+)', 'order by desc (\\1)', sparql, flags=re.IGNORECASE)
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
    query_form_pattern = r'^.*?where'
    query_form_match = re.search(query_form_pattern, query, re.IGNORECASE)
    if query_form_match:
        letter_pattern = r'\?(\w)'
        variables = re.findall(letter_pattern, query_form_match.group(0))
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
