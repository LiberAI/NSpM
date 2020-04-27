#!/usr/bin/env python
"""

Neural SPARQL Machines - Filter dataset by a given criterion.

'SPARQL as a Foreign Language' by Tommaso Soru and Edgard Marx et al., SEMANTiCS 2017
https://arxiv.org/abs/1708.07624

Version 1.0.0

"""
import argparse
import collections
import json
import os
import sys

from generator_utils import encode, save_cache, extract_encoded_entities
import importlib

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('--dataset', dest='dataset', metavar='data_300.en', help='dataset', required=True)
    requiredNamed.add_argument('--used_resources', dest='used_resources', metavar='used_resources.json', help='json file', required=True)
    requiredNamed.add_argument('--minimum', dest='minimum', metavar='15', help='minimum number of occurence', required=True)
    requiredNamed.add_argument('--comp', dest='comp', metavar='all|any', help='require minimum for all/any resources in the query', required=True)
    args = parser.parse_args()

    dataset_file = args.dataset
    used_resources_file = args.used_resources
    MINIMUM = int(args.minimum)
    COMP = any if args.comp == 'any' else all

    importlib.reload(sys)
    sys.setdefaultencoding("utf-8")


    dataset_root, _ = os.path.splitext(dataset_file)
    used_resources_root, _ = os.path.splitext(used_resources_file)
    filtered_sparql_file = '{}_filtered_{:d}_{}.sparql'.format(dataset_root, MINIMUM, COMP.__name__)
    filtered_en_file = '{}_filtered_{:d}_{}.en'.format(dataset_root, MINIMUM, COMP.__name__)

    used_resources = collections.Counter(json.loads(open(used_resources_file).read()))
    filtered_resources = [elem_cnt for elem_cnt in list(used_resources.items()) if elem_cnt[1] >= MINIMUM]
    save_cache('{}_filter_{:d}.json'.format(used_resources_root, MINIMUM), collections.Counter(dict(filtered_resources)))
    valid_encoded_resources = [encode(elem_cnt1[0]) for elem_cnt1 in filtered_resources]
    check = lambda encoded_entity : encoded_entity in valid_encoded_resources

    valid_lines = []
    filtered_queries = []
    with open(dataset_root+'.sparql', 'r') as sparql_file:
        for linenumber, line in enumerate(sparql_file):
            entities = extract_encoded_entities(line)
            valid = COMP(list(map(check, entities)))
            if valid:
                filtered_queries.append(line)
                valid_lines.append(linenumber)

    filtered_questions = []
    with open(dataset_root+'.en', 'r') as en_file:
        for linenumber, line in enumerate(en_file):
            if linenumber in valid_lines:
                filtered_questions.append(line)

    with open(filtered_en_file, 'w') as filtered:
        filtered.writelines(filtered_questions)

    with open(filtered_sparql_file, 'w') as filtered:
        filtered.writelines(filtered_queries)
