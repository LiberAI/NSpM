#!/usr/bin/env python
"""

Neural SPARQL Machines - Generator utils.

'SPARQL as a Foreign Language' by Tommaso Soru and Edgard Marx et al., SEMANTiCS 2017
https://arxiv.org/abs/1708.07624

Version 1.0.0

"""
import collections
import http.client
import json
import logging
import re
import sys
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
from functools import reduce

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


def strip_brackets(s):
    s = re.sub(r'\([^)]*\)', '', s)
    if "," in s:
        s = s[:s.index(",")]
    return s.strip().lower()


REPLACEMENTS = [
    ['dbo:', 'http://dbpedia.org/ontology/', 'dbo_'],
    ['dbp:', 'http://dbpedia.org/property/', 'dbp_'],
    ['dbc:', 'http://dbpedia.org/resource/Category:', 'dbc_'],
    ['dbr:', 'res:', 'http://dbpedia.org/resource/', 'dbr_'],
    ['dct:', 'dct_'],
    ['geo:', 'geo_'],
    ['georss:', 'georss_'],
    ['rdf:', 'rdf_'],
    ['rdfs:', 'rdfs_'],
    ['foaf:', 'foaf_'],
    ['owl:', 'owl_'],
    ['yago:', 'yago_'],
    ['skos:', 'skos_'],
    [' ( ', '  par_open  '],
    [' ) ', '  par_close  '],
    ['(', ' attr_open '],
    [') ', ')', ' attr_close '],
    ['{', ' brack_open '],
    ['}', ' brack_close '],
    [' . ', ' sep_dot '],
    ['. ', ' sep_dot '],
    ['?', 'var_'],
    ['*', 'wildcard'],
    [' <= ', ' math_leq '],
    [' >= ', ' math_geq '],
    [' < ', ' math_lt '],
    [' > ', ' math_gt ']
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
    sparql = decode(encoded_sparql)
    entities = extract_entities(sparql)
    encoded_entities = list(map(encode, entities))
    return encoded_entities


def extract_entities( sparql ):
    triples = extractTriples(sparql)
    entities = set()
    for triple in triples:
        possible_entities = [triple['subject'], triple['object']]
        sorted_out = [e for e in possible_entities if not e.startswith('?') and ':' in e]
        entities = entities.union([re.sub(r'^optional{', '', e, flags=re.IGNORECASE) for e in sorted_out])
    return entities


def extract_predicates( sparql ):
    triples = extractTriples(sparql)
    predicates = set()
    for triple in triples:
        pred = triple['predicate']
        predicates.add(pred)
    return predicates


def extractTriples (sparqlQuery):
    triples = []
    whereStatementPattern = r'where\s*?{(.*?)}'
    whereStatementMatch = re.search(whereStatementPattern, sparqlQuery, re.IGNORECASE)
    if whereStatementMatch:
        whereStatement = whereStatementMatch.group(1)
        triples = splitIntoTriples(whereStatement)
    return triples


def splitIntoTriples (whereStatement):
    tripleAndSeparators = re.split(r'(\.[\s\?\<$])', whereStatement)
    trimmed = [str.strip() for str in tripleAndSeparators]

    def repair (list, element):
        if element not in ['.', '.?', '.<']:
            previousElement = list[-1]
            del list[-1]
            if previousElement in ['.', '.?', '.<']:
                cutoff = previousElement[1] if previousElement in ['.?', '.<'] else ''
                list.append(cutoff + element)
            else:
                list.append(previousElement + ' ' + element)
        else:
            list.append(element)

        return list

    tripleStatements = reduce(repair, trimmed, [''])
    triplesWithNones = list(map(splitIntoTripleParts, tripleStatements))
    triples = [triple for triple in triplesWithNones if triple != None]
    return triples


def splitIntoTripleParts (triple):
    statementPattern = r'(\S+)\s+(\S+)\s+(\S+)'
    statementPatternMatch = re.search(statementPattern, triple)

    if statementPatternMatch:
        return {
            'subject': statementPatternMatch.group(1),
            'predicate': statementPatternMatch.group(2),
            'object': statementPatternMatch.group(3)
        }
    else:
        return None

def fix_URI(query):
	query = re.sub(r"dbr:([^\s]+)" , r"<http://dbpedia.org/resource/\1>" , query)
	if query[-2:]=="}>":
		query = query[:-2]+">}"
	return query
