#!/usr/bin/env python
"""

Neural SPARQL Machines - Generator module

'SPARQL as a Foreign Language' by Tommaso Soru and Edgard Marx et al., SEMANTiCS 2017
https://w3id.org/neural-sparql-machines/soru-marx-semantics2017.html
https://arxiv.org/abs/1708.07624

"""
import argparse
import logging
import operator
import os
import random
import sys
import traceback
import urllib2, urllib, httplib, json
import re

import datetime

logging.basicConfig(filename='generator.log', level=logging.DEBUG)
ENDPOINT = "http://dbpedia.org/sparql"
GRAPH = "http://dbpedia.org"
EXAMPLES_PER_TEMPLATE = 300
CELEBRITY_LIST = ['http://dbpedia.org/class/yago/Wikicat21st-centuryActors',
                  'http://dbpedia.org/class/yago/WikicatPresidentsOfTheUnitedStates',
                  'dbo:Royalty',
                  'http://dbpedia.org/class/yago/Honoree110183757'
                  ]


def count_usage ( resource ):
    if resource in used_resources:
        used_resources[resource] += 1
    else:
        used_resources[resource] = 1


def log_statistics ( used_resources ):
    statistics = {}
    total_number_of_resources = len(used_resources)
    for resource in used_resources:
        usages = used_resources[resource]
        if usages in statistics:
            statistics[usages] += 1
        else:
            statistics[usages] = 1
    logging.info('{:6d} used resources'.format(total_number_of_resources))
    for usage in statistics:
        logging.info('{:6d} resources occur \t{:6d} times \t({:6.2f} %) '.format(statistics[usage], usage, statistics[usage]*100/total_number_of_resources))


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

def extract_bindings( data, template ):
    matches = list()
    for match in data:
        matches.append(match)

    random.shuffle(matches)
    logging.debug('{} matches for {}'.format(len(matches), getattr(template, 'id')))

    if len(matches) == 0:
        return None

    if len(matches) <= EXAMPLES_PER_TEMPLATE:
        best_matches = matches
    else:
        best_matches = sort_matches(matches, template)[0:EXAMPLES_PER_TEMPLATE]

    bindings = list()
    variables = getattr(template, 'variables')

    for match in best_matches:
        pairs = []
        for variable in variables:
            resource = match[variable]["value"]
            label = match["l" + variable]["value"]
            pairs.extend([resource, label])
            count_usage(resource)
            # logging.debug("resource = {} -> {}".format(resource, label))
        bindings.append(pairs)
        
    return bindings


def sort_matches( matches, template ):
    variables = getattr(template, 'variables')
    get_usages = lambda match : map(lambda variable : get_number_of_usages(match[variable]["value"]), variables)

    matches_with_usages = map(lambda match : {'usages': get_usages(match), 'match': match}, matches)
    sorted_matches_with_usages = sorted(matches_with_usages, key=prioritize_usage)
    sorted_matches = map(operator.itemgetter('match'), sorted_matches_with_usages)

    return sorted_matches


def get_number_of_usages ( uri ):
    if uri in used_resources:
        return used_resources[uri]
    return 0


def prioritize_usage ( match ):
    usages = match['usages']
    if len(usages) == 1:
        return prioritize_single_match(usages[0])
    else:
        if len(usages) == 2:
            return prioritize_couple_match(usages)
        else:
            return prioritize_triple_match(usages)

def prioritize_single_match( usage ):
    # realises prioritity: 2 < 1 < 0 < 3
    highest_priority = usage == 2
    second_highest_priority = usage == 1
    third_highest_priority = usage == 0
    if highest_priority:
        return 0
    if second_highest_priority:
        return 1
    if third_highest_priority:
        return 2
    return usage


def prioritize_couple_match( usages ):
    usage, other_usage = usages
    highest_priority = usages == [2, 2]
    second_highest_priority = usages in [[2, 1], [1, 2]]
    third_highest_priority = usages == [1, 1]
    fourth_highest_priority = usages in [[0, 1], [1, 0]]
    fifth_highest_priority = (usage == 2 and other_usage <= 10) or (other_usage == 2 and usage <= 10)
    sixth_highest_priority = (usage == 1 and other_usage <= 10) or (other_usage == 1 and usage <= 10)
    seventh_highest_priority = usages == [0, 0]

    if highest_priority:
        return 0
    if second_highest_priority:
        return 1
    if third_highest_priority:
        return 2
    if fourth_highest_priority:
        return 3
    if fifth_highest_priority:
        return 4
    if sixth_highest_priority:
        return 5
    if seventh_highest_priority:
        return 6
    # smallest not prioritized pair is (3,0)
    return sum(usages) + 4

def prioritize_triple_match( usages ):
    between_zero_and_three = lambda value : value > 0 and value < 3
    highest_priority = all(map(between_zero_and_three, usages))
    second_highest_priority = filter(between_zero_and_three, usages) > 1
    third_highest_priority = any(map(between_zero_and_three, usages))

    if highest_priority:
        return 0
    if second_highest_priority:
        return 1
    if third_highest_priority:
        return 2

    return sum(usages)


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

class Annotation:
    def __init__(self, question, query, generator_query, id=None, target_classes=None):
        self.question = question
        self.query = query
        self.generator_query = generator_query
        self.id = id
        self.target_classes = target_classes if target_classes != None else []
        self.variables = extract_variables(generator_query)

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

def build_dataset_pair(binding, template):
    english_template_question = getattr(template, 'question')
    sparql_template_query = getattr(template, 'query')
    uri_a = binding[0]
    label_a = binding[1]
    english = english_template_question.replace("<A>", strip_brackets(label_a))
    sparql = sparql_template_query.replace("<A>", uri_a)
    has_more_than_one_placeholder = len(getattr(template, 'variables')) > 1
    if has_more_than_one_placeholder:
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
        if "<C>" in english:
            label_c = binding[5]
            if label_c is not None:
                english = english.replace("<C>", strip_brackets(label_c))
            else:
                return None
        if "<C>" in sparql:
            uri_c = binding[4]
            if uri_c is not None:
                sparql = sparql.replace("<C>", uri_c)
            else:
                return None
    sparql = replacements(sparql)
    dataset_pair = {'english': english, 'sparql': sparql}
    return dataset_pair


def extract_variables(query):
    variables = []
    variable_pattern = r'select\s(distinct)?(.*?)where'
    variable_match = re.search(variable_pattern, query, re.IGNORECASE)
    if variable_match:
        letter_pattern = r'\?(\w)'
        variables = re.findall(letter_pattern, variable_match.group((2)))
    return variables


def generate_dataset(templates, output_dir, file_mode):
    cache = dict()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_dir + '/data_300.en', file_mode) as english_questions:
        with open(output_dir + '/data_300.sparql', file_mode) as sparql_queries:
            for template in templates:
                try:
                    results = get_results_of_generator_query(cache, template)
                    bindings = extract_bindings(results["results"]["bindings"], template)

                    if bindings is None:
                        logging.debug("no data for {}".format(getattr(template, 'id')))
                        continue

                    for binding in bindings:
                        dataset_pair = build_dataset_pair(binding, template)

                        if (dataset_pair):
                            english_questions.write("{}\n".format(dataset_pair['english']))
                            sparql_queries.write("{}\n".format(dataset_pair['sparql']))
                except:
                    exception = traceback.format_exc()
                    logging.error('template {} caused exception {}'.format(getattr(template, 'id'), exception))
                    logging.info('1. fix problem\n2. remove templates until the exception template in the template file\n3. restart with `--continue` parameter')
                    raise Exception()


def get_results_of_generator_query( cache, template ):
    generator_query = getattr(template, 'generator_query')

    if generator_query in cache:
        results = cache[generator_query]
    else:
        query = prepare_generator_query(template)
        logging.debug('ready generator_query: ' + query)
        results = query_dbpedia(query)
        cache[generator_query] = results
    return results


def prepare_generator_query( template ):
    generator_query = getattr(template, 'generator_query')
    target_classes = getattr(template, 'target_classes')
    variables = getattr(template, 'variables')

    def variable_is_subclass ( query, variable ):
        predicate_pattern = r'\s+?(rdf:type|a)\s+?\?' + variable
        predicate_match = re.search(predicate_pattern, query)
        return bool(predicate_match)

    add_requirement = lambda query, where_replacement: query.replace(" where { ", where_replacement)
    LABEL_REPLACEMENT = " , (str(?lab%(variable)s) as ?l%(variable)s) where { ?%(variable)s rdfs:label ?lab%(variable)s . FILTER(lang(?lab%(variable)s) = 'en') . "
    CLASS_REPLACEMENT = " where { ?%(variable)s a %(class)s . "
    SUBCLASS_REPLACEMENT = " where { ?%(variable)s rdfs:subClassOf %(class)s . "


    for i, variable in enumerate(variables):
        generator_query = add_requirement(generator_query, LABEL_REPLACEMENT % {'variable': variable})
        variable_has_a_type = len(target_classes) > i and target_classes[i]
        if variable_has_a_type:
            if variable_is_subclass(generator_query, variable):
                generator_query = add_requirement(generator_query, SUBCLASS_REPLACEMENT % {'variable': variable, 'class': target_classes[i]})
            else:
                # if target_classes[i] == 'dbo:Person':
                #     target_class = random.choice(CELEBRITY_LIST)
                # else:
                target_class = target_classes[i]
                generator_query = add_requirement(generator_query, CLASS_REPLACEMENT % {'variable': variable, 'class': target_class})

    return generator_query


def saveCache (file, cache):
    with open(file, 'w') as outfile:
        json.dump(cache, outfile)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--continue', dest='continue_generation', action='store_true', help='Continue after exception')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('--templates', dest='templates', metavar='templateFile', help='templates', required=True)
    requiredNamed.add_argument('--output', dest='output', metavar='outputDirectory', help='dataset directory', required=True)
    args = parser.parse_args()

    template_file = args.templates
    output_dir = args.output
    use_resources_dump = args.continue_generation
    RESOURCE_DUMP_FILE = 'resource_dump.json'
    resource_dump_exists = os.path.exists(RESOURCE_DUMP_FILE)

    if (resource_dump_exists and not use_resources_dump):
        warning_message = 'Warning: The file {} exists which indicates an error. Remove file or continue generation after fixing with --continue'.format(
            RESOURCE_DUMP_FILE)
        print warning_message
    else:
        reload(sys)
        sys.setdefaultencoding("utf-8")

        used_resources = json.loads(open(RESOURCE_DUMP_FILE).read()) if use_resources_dump else dict()
        file_mode = 'a' if use_resources_dump else 'w'
        templates = read_template_file(template_file)
        try:
            generate_dataset(templates, output_dir, file_mode)
        except:
            print 'exception occured, look for error in log file'
        finally:
            log_statistics(used_resources)
            saveCache('used_resources_{:%Y-%m-%d-%H-%M}.json'.format(datetime.datetime.today()), used_resources)
