#!/usr/bin/env python
"""

Neural SPARQL Machines - Generator module

'SPARQL as a Foreign Language' by Tommaso Soru and Edgard Marx et al., SEMANTiCS 2017
https://w3id.org/neural-sparql-machines/soru-marx-semantics2017.html
https://arxiv.org/abs/1708.07624

"""
import argparse
import collections
import datetime
import json
import logging
import operator
import os
import random
import re
import sys
import traceback

from generator_utils import log_statistics, saveCache, query_dbpedia, strip_brackets, replacements, read_template_file

CELEBRITY_LIST = [
    'dbo:Royalty',
    '<http://dbpedia.org/class/yago/Wikicat21st-centuryActors>',
    '<http://dbpedia.org/class/yago/Wikicat20th-centuryNovelists>',
    '<http://dbpedia.org/class/yago/Honoree110183757>'
    ]

SPECIAL_CLASSES = {
    'dbo:Person': ['dbo:TableTennisPlayer'],
    'dbo:Athlete': ['dbo:TableTennisPlayer']
}
EXAMPLES_PER_TEMPLATE = 300

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
        binding = {}
        for variable in variables:
            resource = match[variable]["value"]
            label = match["l" + variable]["value"]
            binding[variable] = {'uri': resource, 'label': label}
            used_resources.update([resource])
        bindings.append(binding)
        
    return bindings


def sort_matches( matches, template ):
    variables = getattr(template, 'variables')
    get_usages = lambda match : map(lambda variable : used_resources[match[variable]["value"]], variables)

    matches_with_usages = map(lambda match : {'usages': get_usages(match), 'match': match}, matches)
    sorted_matches_with_usages = sorted(matches_with_usages, key=prioritize_usage)
    sorted_matches = map(operator.itemgetter('match'), sorted_matches_with_usages)

    return sorted_matches

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
    highest_priority = 30 > usage > 0
    second_highest_priority = usage == 0
    if highest_priority:
        return 0
    if second_highest_priority:
        return 1
    return usage


def prioritize_couple_match( usages ):
    between_zero_and_upper_limit = lambda value : 0 < value < 30
    usage, other_usage = usages
    highest_priority = all(map(between_zero_and_upper_limit, usages))
    second_highest_priority = any(map(between_zero_and_upper_limit, usages))
    third_highest_priority = usage == 0 and other_usage == 0

    if highest_priority:
        return 0
    if second_highest_priority:
        return 1
    if third_highest_priority:
        return 2
    return sum(usages)

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


def build_dataset_pair(binding, template):
    english = getattr(template, 'question')
    sparql = getattr(template, 'query')
    for variable in binding:
        uri = binding[variable]['uri']
        label = binding[variable]['label']
        placeholder = '<{}>'.format(str.upper(variable))
        if placeholder in english and label is not None:
            english = english.replace(placeholder, strip_brackets(label))
        if placeholder in sparql and uri is not None:
            sparql = sparql.replace(placeholder, uri)

    sparql = replacements(sparql)
    dataset_pair = {'english': english, 'sparql': sparql}
    return dataset_pair


def generate_dataset(templates, output_dir, file_mode):
    cache = dict()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_dir + '/data_300.en', file_mode) as english_questions, open(output_dir + '/data_300.sparql', file_mode) as sparql_queries:
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

LABEL_REPLACEMENT = " , (str(?lab{variable}) as ?l{variable}) where {{ ?{variable} rdfs:label ?lab{variable} . FILTER(lang(?lab{variable}) = 'en') . "
CLASS_REPLACEMENT = " where {{ ?{variable} a {ontology_class} . "
CLASSES_REPLACEMENT = " where {{ ?{variable} a ?t . VALUES (?t) {{ {classes} }} . "
SUBCLASS_REPLACEMENT = " where {{ ?{variable} rdfs:subClassOf {ontology_class} . "

def prepare_generator_query( template ):
    generator_query = getattr(template, 'generator_query')
    target_classes = getattr(template, 'target_classes')
    variables = getattr(template, 'variables')

    def variable_is_subclass ( query, variable ):
        predicate_pattern = r'\s+?(rdf:type|a)\s+?\?' + variable
        predicate_match = re.search(predicate_pattern, query)
        return bool(predicate_match)

    add_requirement = lambda query, where_replacement: query.replace(" where { ", where_replacement)


    for i, variable in enumerate(variables):
        generator_query = add_requirement(generator_query, LABEL_REPLACEMENT.format(variable=variable))
        variable_has_a_type = len(target_classes) > i and target_classes[i]
        if variable_has_a_type:
            if variable_is_subclass(generator_query, variable):
                generator_query = add_requirement(generator_query, SUBCLASS_REPLACEMENT.format(variable=variable, ontology_class=target_classes[i]))
            else:
                if target_classes[i] in SPECIAL_CLASSES:
                    classes = ' '.join(map(lambda c : '({})'.format(c), SPECIAL_CLASSES[target_classes[i]]))
                    generator_query = add_requirement(generator_query, CLASSES_REPLACEMENT.format(variable=variable,classes=classes))
                else:
                    ontology_class = target_classes[i]
                    generator_query = add_requirement(generator_query, CLASS_REPLACEMENT.format(variable=variable, ontology_class=ontology_class))
    return generator_query


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

    time = datetime.datetime.today()
    logging.basicConfig(filename='{}/generator_{:%Y-%m-%d-%H-%M}.log'.format(output_dir, time), level=logging.DEBUG)
    resource_dump_file = output_dir + '/resource_dump.json'
    resource_dump_exists = os.path.exists(resource_dump_file)

    if (resource_dump_exists and not use_resources_dump):
        warning_message = 'Warning: The file {} exists which indicates an error. Remove file or continue generation after fixing with --continue'.format(
            resource_dump_file)
        print warning_message
        sys.exit(1)

    reload(sys)
    sys.setdefaultencoding("utf-8")

    used_resources = collections.Counter(json.loads(open(resource_dump_file).read())) if use_resources_dump else collections.Counter()
    file_mode = 'a' if use_resources_dump else 'w'
    templates = read_template_file(template_file)
    try:
        generate_dataset(templates, output_dir, file_mode)
    except:
        print 'exception occured, look for error in log file'
        saveCache(resource_dump_file, used_resources)
    else:
        saveCache('{}/used_resources_{:%Y-%m-%d-%H-%M}.json'.format(output_dir, time), used_resources)
    finally:
        log_statistics(used_resources)