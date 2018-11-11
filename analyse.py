#!/usr/bin/env python
"""

Neural SPARQL Machines - Analysis and validation of translated questions into queries.

'SPARQL as a Foreign Language' by Tommaso Soru and Edgard Marx et al., SEMANTiCS 2017
https://w3id.org/neural-sparql-machines/soru-marx-semantics2017.html
https://arxiv.org/abs/1708.07624

Version 0.1.0-akaha

"""
import argparse
import collections
import json
import os
import re
import sys
import urllib
from pyparsing import ParseException
from rdflib.plugins.sparql import parser

from generator_utils import decode, extract_entities, extract_predicates


def analyse( translation ):
    result = {}
    for test in TESTS:
        result[test] = TESTS[test](translation)

    everything_okay = all(map(lambda test: result[test], TESTS))
    details['everything_okay'].update([everything_okay])

    return result


def validate( translation ):
    _, query = translation
    # encode slash in prefix uri
    entity_with_attribute = r'\w+:\w+\(<?\w+>?\)'
    match = re.search(entity_with_attribute, query)
    if match:
        entity = match.group(0)
        entity_encoded = re.sub(r'\(<?', '\(', entity)
        entity_encoded = re.sub(r'>?\)', '\)', entity_encoded)
        query = query.replace(entity, entity_encoded)
    try:
        parser.parseQuery(query)
    except ParseException as exception:
        print '{} in "{}", loc: {}'.format(exception.msg, exception.line, exception.loc)
        details['parse_exception'].update([exception.msg])
        return False
    except Exception as exception:
        msg = str(exception)
        print '{}'.format(msg)
        details['other_exception'].update([msg])
        return False
    else:
        return True


def check_type( translation ):
    target, generated = translation
    target_type = extract_type(target)
    return target_type == extract_type(generated) and target_type is not None


def extract_type( query ):
    result_description = extract_result_description(query)
    types = [r'select.*?count.*?where', 'select', 'ask', 'describe']
    for query_type in types:
        match = re.search(query_type, result_description, re.IGNORECASE)
        if match:
            return query_type
    return None


def extract_result_description (sparqlQuery):
    selectStatementPattern = r'(.*?)\swhere'
    selectStatementMatch = re.search(selectStatementPattern, sparqlQuery, re.IGNORECASE)
    if selectStatementMatch:
        return selectStatementMatch.group(1)
    return ''


def check_entities ( translation ):
    target, generated = translation
    entities = extract_entities(target)
    if not entities:
        return False
    entities_detected = map(lambda entity : entity in generated, entities)
    entities_with_occurence_count = map(lambda entity: '{} [{}]'.format(entity, get_occurence_count(entity)), entities)
    if all(entities_detected):
        details['detected_entity'].update(entities_with_occurence_count)
        return True

    if any(entities_detected):
        details['partly_detected_entities'].update([True])

    details['undetected_entity'].update(map(lambda (entity, detected) : entity, filter(lambda (entity, detected) : not detected, zip(entities_with_occurence_count, entities_detected))))
    return False


def check_predicates ( translation, ignore_prefix=True, ignore_case=True ):
    strip_prefix = lambda entity : entity[entity.find(':') :]
    target, generated = translation
    predicates = extract_predicates(target)
    if not predicates:
        return False
    if ignore_prefix:
        predicates = map(strip_prefix, predicates)
    if ignore_case:
        predicates = map(str.lower, predicates)
        generated = str.lower(generated)
    predicates_detected = map(lambda predicate: predicate in generated, predicates)
    if all(predicates_detected):
        return True

    if any(predicates_detected):
        details['partly_detected_predicates'].update([True])

    details['undetected_predicates'].update(map(lambda (predicate, detected): predicate,
                                            filter(lambda (predicate, detected): not detected,
                                                   zip(predicates, predicates_detected))))
    return False


def summarise( summary, current_evaluation ):
    for test in TESTS:
        test_result = current_evaluation[test]
        summary[test].update([test_result])
    return summary


def log_summary( summary, details, org_file, ask_output_file ):
    print '\n\nSummary\n'
    print 'Analysis based on {} and {}'.format(org_file, ask_output_file)
    for test in TESTS:
        print '{:30}: {:6d} True / {:6d} False'.format(test, summary[test][True], summary[test][False])
    print '{:30}: {:6d} True / {:6d} False'.format('everything_okay', details['everything_okay'][True], details['everything_okay'][False])
    print '\n\nDetails\n'
    for detail in details:
        for key in details[detail]:
            print '{:30}: {:6d} {}'.format(detail, details[detail][key], key)


def read( file_name ):
    with open(file_name) as file:
        questions = file.readlines()
    return questions


def get_occurence_count ( entity ):
    key = unicode(entity)
    occurence_count = used_entities_counter[key] if key in used_entities_counter else 0
    if not occurence_count:
        key += '.'
        occurence_count = used_entities_counter[key] if key in used_entities_counter else 0
        if not occurence_count:
            print 'not found: {}'.format(entity)
    return occurence_count


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    requiredNamed = arg_parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('--target', dest='target', metavar='test.sparql', help='encoded sparql queries', required=True)
    requiredNamed.add_argument('--generated', dest='generated', metavar='nmt/output.txt', help='direct (encoded) NSpM output', required=True)
    args = arg_parser.parse_args()

    targets_file = args.target
    ask_output_file = args.generated

    reload(sys)
    sys.setdefaultencoding("utf-8")

    TESTS = {
        'valid_sparql': validate,
        'correct_query_type': check_type,
        'entities_detected': check_entities,
        'predicates_detected': check_predicates
    }

    details = {
        'parse_exception': collections.Counter(),
        'other_exception': collections.Counter(),
        'detected_entity': collections.Counter(),
        'undetected_entity': collections.Counter(),
        'partly_detected_entities': collections.Counter(),
        'partly_detected_predicates': collections.Counter(),
        'undetected_predicates': collections.Counter(),
        'everything_okay': collections.Counter()
    }

    directory = os.path.dirname(ask_output_file)
    used_entities_counter = json.load(open('{}/used_resources_normalized.json'.format(directory)))
    encoded_targets = read(targets_file)
    encoded_generated = read(ask_output_file)

    if len(encoded_targets) != len(encoded_generated):
        print 'Some translations are missing'
        sys.exit(1)

    targets = map(decode, encoded_targets)
    generated = map(decode, encoded_generated)
    translations = zip(targets, generated)
    evaluation = map(analyse, translations)
    summary_obj = {}
    for test in TESTS:
        summary_obj[test] = collections.Counter()

    summary = reduce(summarise, evaluation, summary_obj)
    log_summary(summary, details, targets_file, ask_output_file)