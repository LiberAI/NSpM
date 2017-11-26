import collections
import logging
import re
import sys

from pyparsing import ParseException
from rdflib.plugins.sparql import parser
from generator_utils import decode


def analyse( translation ):
    result = {}
    for test in TESTS:
        result[test] = TESTS[test](translation)
    return result


def validate( translation ):
    _, query = translation
    # rdflib parser does not accept parantheses in URIs
    rdflib_parser_valid_parentheses_open = '\('
    rdflib_parser_valid_parentheses_close = '\)'
    query = query.replace('(', rdflib_parser_valid_parentheses_open)
    query = query.replace(')', rdflib_parser_valid_parentheses_close)
    try:
        parser.parseQuery(query)
    except ParseException as exception:
        logging.debug('{} in "{}", loc: {}'.format(exception.msg, exception.line, exception.loc))
        details['parse_exception'].update([exception.msg])
        return False
    else:
        return True


def check_type( translation ):
    original, generated = translation
    original_type = extract_type(original)
    return original_type == extract_type(generated) and original_type is not None


def extract_type( query ):
    result_description = extract_result_description(query)
    types = ['ask', 'describe', 'select']
    for query_type in types:
        match = re.search(query_type, result_description, re.IGNORECASE)
        if match:
            return query_type
    return None


def extract_result_description (sparqlQuery):
    selectStatementPattern = r'(.*?)\swhere'
    selectStatementMatch = re.search(selectStatementPattern, sparqlQuery, re.IGNORECASE)
    selectStatement = selectStatementMatch.group(1)
    return selectStatement


def summarise( summary, current_evaluation ):
    for test in TESTS:
        test_result = current_evaluation[test]
        summary[test].update([test_result])
    return summary


def log_summary( summary, details, org_file, ask_output_file ):
    logging.info('Analysis based on {} and {}'.format(org_file, ask_output_file))
    for test in TESTS:
        logging.info('{:30}: {:6d} True / {:6d} False'.format(test, summary[test][True], summary[test][False]))
    for detail in details:
        for key in details[detail]:
            logging.info('{:30}: {:6d} {}'.format(detail, details[detail][key], key))


def read( file_name ):
    with open(file_name) as file:
        questions = file.readlines()
    return questions


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding("utf-8")
    logging.basicConfig(filename='analysis.log', level=logging.DEBUG)

    TESTS = {
        'valid_sparql': validate,
        'correct_query_type': check_type
    }

    details = {
        'parse_exception': collections.Counter()
    }

    originals_file = sys.argv[1]
    ask_output_file = sys.argv[2]

    encoded_originals = read(originals_file)
    encoded_generated = read(ask_output_file)

    if len(encoded_originals) != len(encoded_generated):
        print 'Some translations are missing'
        sys.exit(1)

    originals = map(decode, encoded_originals)
    generated = map(decode, encoded_generated)
    translations = zip(originals, generated)
    evaluation = map(analyse, translations)
    summary_obj = {}
    for test in TESTS:
        summary_obj[test] = collections.Counter()

    summary = reduce(summarise, evaluation, summary_obj)
    log_summary(summary, details, originals_file, ask_output_file)