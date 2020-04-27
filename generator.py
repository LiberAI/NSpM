#!/usr/bin/env python
"""

Neural SPARQL Machines - Generator module.

'SPARQL as a Foreign Language' by Tommaso Soru and Edgard Marx et al., SEMANTiCS 2017
https://arxiv.org/abs/1708.07624

Version 1.0.0

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
from tqdm import tqdm
import io

from generator_utils import log_statistics, save_cache, query_dbpedia, strip_brackets, encode, read_template_file
import importlib

CELEBRITY_LIST = [
    'dbo:Royalty',
    '<http://dbpedia.org/class/yago/Wikicat21st-centuryActors>',
    '<http://dbpedia.org/class/yago/WikicatEnglishMusicians>',
    '<http://dbpedia.org/class/yago/Wikicat20th-centuryNovelists>',
    '<http://dbpedia.org/class/yago/Honoree110183757>'
]

SPECIAL_CLASSES = {
    'dbo:Person': [
        '<http://dbpedia.org/class/yago/Wikicat21st-centuryActors>',
        '<http://dbpedia.org/class/yago/WikicatEnglishMusicians>',
        '<http://dbpedia.org/class/yago/Wikicat20th-centuryNovelists>',
        '<http://dbpedia.org/class/yago/Honoree110183757>',
        'dbo:LacrossePlayer'
    ],
    'dbo:Athlete': ['dbo:LacrossePlayer'],
    'dbo:SportsTeam': ['dboBasketballTeam']
}
EXAMPLES_PER_TEMPLATE = 600


def extract_bindings(data, template):
    matches = list()
    for match in data:
        matches.append(match)

    random.shuffle(matches)
    logging.debug('{} matches for {}'.format(
        len(matches), getattr(template, 'id')))

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


def sort_matches(matches, template):
    variables = getattr(template, 'variables')
    def get_usages(match): return [
        used_resources[match[variable]["value"]] for variable in variables]

    matches_with_usages = [{'usages': get_usages(
        match), 'match': match} for match in matches]
    sorted_matches_with_usages = sorted(
        matches_with_usages, key=prioritize_usage)
    sorted_matches = list(
        map(operator.itemgetter('match'), sorted_matches_with_usages))

    return sorted_matches


def prioritize_usage(match):
    usages = match['usages']
    if len(usages) == 1:
        return prioritize_single_match(usages[0])
    else:
        if len(usages) == 2:
            return prioritize_couple_match(usages)
        else:
            return prioritize_triple_match(usages)


def prioritize_single_match(usage):
    highest_priority = 20 >= usage > 10
    second_highest_priority = 30 >= usage > 20
    third_highest_priority = 10 >= usage > 0
    fourth_highest_priority = 50 >= usage > 30
    fifth_highest_priority = usage == 0
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
    return usage


def prioritize_couple_match(usages):
    def between_zero_and_upper_limit(value): return 0 < value < 30
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


def prioritize_triple_match(usages):
    def between_zero_and_upper_limit(value): return 0 < value < 30
    highest_priority = all(map(between_zero_and_upper_limit, usages))
    second_highest_priority = list(
        filter(between_zero_and_upper_limit, usages)) >= 2
    third_highest_priority = any(map(between_zero_and_upper_limit, usages))

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

    sparql = encode(sparql)
    dataset_pair = {'english': english, 'sparql': sparql}
    return dataset_pair


def generate_dataset(templates, output_dir, file_mode):
    cache = dict()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    it = 0
    with io.open(output_dir + '/data_300.en', file_mode, encoding="utf-8") as english_questions, io.open(output_dir + '/data_300.sparql', file_mode, encoding="utf-8") as sparql_queries:
        for template in tqdm(templates):
            it = it + 1
            print("for {}th template".format(it))
            try:
                results = get_results_of_generator_query(cache, template)
                bindings = extract_bindings(
                    results["results"]["bindings"], template)
                # print bindings
                if bindings is None:
                    id_or_question = getattr(
                        template, 'id') or getattr(template, 'question')
                    logging.debug("no data for {}".format(id_or_question))
                    not_instanced_templates.update([id_or_question])
                    continue

                for binding in bindings:
                    dataset_pair = build_dataset_pair(binding, template)
                    # print "x", det_pair
                    if (dataset_pair):
                        dataset_pair['english'] = " ".join(
                            dataset_pair['english'].split())
                        english_questions.write(
                            "{}\n".format(dataset_pair['english']))
                        dataset_pair['sparql'] = re.sub(
                            r"\s\s+", " ", dataset_pair['sparql'])
                        a = re.search('(.*)brack_open', dataset_pair['sparql'])
                        b = re.search('brack_open(.*)brack_close',
                                      dataset_pair['sparql'])
                        c = re.search('brack_close(.*)',
                                      dataset_pair['sparql'])
                        # print a.group(1),b.group(1)
                        a = a.group(1)
                        b = b.group(1)
                        c = c.group(1)
                        b = b.replace(' attr_open ', '(')
                        b = b.replace(' attr_close', ')')
                        dataset_pair['sparql'] = a + \
                            ' brack_open ' + b + ' brack_close ' + c
                        dataset_pair['sparql'] = " ".join(
                            dataset_pair['sparql'].split())

                        sparql_queries.write(
                            "{}\n".format(dataset_pair['sparql']))
            except:
                exception = traceback.format_exc()
                logging.error('template {} caused exception {}'.format(
                    getattr(template, 'id'), exception))
                logging.info(
                    '1. fix problem\n2. remove templates until the exception template in the template file\n3. restart with `--continue` parameter')
                raise Exception()


def get_results_of_generator_query(cache, template):
    generator_query = getattr(template, 'generator_query')
    def first_attempt(template): return prepare_generator_query(template)
    def second_attempt(template): return prepare_generator_query(
        template, do_special_class_replacement=False)
    def third_attempt(template): return prepare_generator_query(
        template, add_type_requirements=False)

    for attempt, prepare_query in enumerate([first_attempt, second_attempt, third_attempt], start=1):
        query = prepare_query(template)
        if query in cache:
            results = cache[query]
            break
        logging.debug('{}. attempt generator_query: {}'.format(attempt, query))
        results = query_dbpedia(query)
        sufficient_examples = len(
            results["results"]["bindings"]) >= EXAMPLES_PER_TEMPLATE/3
        if sufficient_examples:
            cache[query] = results
            break
    return results


LABEL_REPLACEMENT = "  (str(?lab{variable}) as ?l{variable}) where {{ ?{variable} rdfs:label ?lab{variable} . FILTER(lang(?lab{variable}) = 'en') . "
CLASS_REPLACEMENT = " where {{ ?{variable} a {ontology_class} . "
CLASSES_REPLACEMENT = " where {{ ?{variable} a ?t . VALUES (?t) {{ {classes} }} . "
SUBCLASS_REPLACEMENT = " where {{ ?{variable} rdfs:subClassOf {ontology_class} . "


def variable_is_subclass(query, variable):
    predicate_pattern = r'\s+?(rdf:type|a)\s+?\?' + variable
    predicate_match = re.search(predicate_pattern, query)
    return bool(predicate_match)


def add_requirement(query, where_replacement):
    return query.replace(" where { ", where_replacement)


def prepare_generator_query(template, add_type_requirements=True, do_special_class_replacement=True):
    generator_query = getattr(template, 'generator_query')
    target_classes = getattr(template, 'target_classes')
    variables = getattr(template, 'variables')

    for i, variable in enumerate(variables):
        generator_query = add_requirement(
            generator_query, LABEL_REPLACEMENT.format(variable=variable))
        variable_has_a_type = len(target_classes) > i and target_classes[i]
        if variable_has_a_type and add_type_requirements:
            normalized_target_class = normalize(target_classes[i])
            if variable_is_subclass(generator_query, variable):
                generator_query = add_requirement(generator_query, SUBCLASS_REPLACEMENT.format(
                    variable=variable, ontology_class=normalized_target_class))
            else:
                if normalized_target_class in SPECIAL_CLASSES and do_special_class_replacement:
                    classes = ' '.join(
                        ['({})'.format(c) for c in SPECIAL_CLASSES[normalized_target_class]])
                    generator_query = add_requirement(
                        generator_query, CLASSES_REPLACEMENT.format(variable=variable, classes=classes))
                else:
                    ontology_class = normalized_target_class
                    generator_query = add_requirement(generator_query, CLASS_REPLACEMENT.format(
                        variable=variable, ontology_class=ontology_class))
    return generator_query


def normalize(ontology_class):
    if str.startswith(ontology_class, 'http://dbpedia.org/ontology/'):
        return str.replace(ontology_class, 'http://dbpedia.org/ontology/', 'dbo:')
    if str.startswith(ontology_class, 'http'):
        return '<{}>'.format(ontology_class)
    return ontology_class


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--continue', dest='continue_generation',
                        action='store_true', help='Continue after exception')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('--templates', dest='templates',
                               metavar='templateFile', help='templates', required=True)
    requiredNamed.add_argument(
        '--output', dest='output', metavar='outputDirectory', help='dataset directory', required=True)
    args = parser.parse_args()

    template_file = args.templates
    output_dir = args.output
    use_resources_dump = args.continue_generation

   # print use_resources_dump => False

    time = datetime.datetime.today()
    logging.basicConfig(
        filename='{}/generator_{:%Y-%m-%d-%H-%M}.log'.format(output_dir, time), level=logging.DEBUG)
    resource_dump_file = output_dir + '/resource_dump.json'
    resource_dump_exists = os.path.exists(resource_dump_file)

    # print resource_dump_file, resource_dump_exists => data/place_v1/resource_dump.json False

    if (resource_dump_exists and not use_resources_dump):
        warning_message = 'Warning: The file {} exists which indicates an error. Remove file or continue generation after fixing with --continue'.format(
            resource_dump_file)
        print(warning_message)
        sys.exit(1)

    importlib.reload(sys)

    not_instanced_templates = collections.Counter()
    used_resources = collections.Counter(json.loads(open(
        resource_dump_file).read())) if use_resources_dump else collections.Counter()
    file_mode = 'a' if use_resources_dump else 'w'
    templates = read_template_file(template_file)

    try:
        generate_dataset(templates, output_dir, file_mode)
    except:
        print('exception occured, look for error in log file')
        save_cache(resource_dump_file, used_resources)
    else:
        save_cache(
            '{}/used_resources_{:%Y-%m-%d-%H-%M}.json'.format(output_dir, time), used_resources)
    finally:
        log_statistics(used_resources, SPECIAL_CLASSES,
                       not_instanced_templates)
