from constant import Constant
import logging
import os
from template_generator import template_generator
# from sentence_and_template_generator import sentence_and_template_generator
from generate_url import generate_url
from get_properties import get_properties
import argparse
import re

import tensorflow as tf
tf.compat.v1.enable_eager_execution()

const = Constant()

def generate_templates(label, project_name, depth=1, output_file="template_generator", multi=False):
    """
    The function acts as a wrapper for the whole package of supplied source code.
    """

    count = 0
    vessel = []
    depth = int(depth)
    if (not os.path.isdir(project_name)):
        os.makedirs(project_name)
    output_file = open(project_name + "/" + output_file, 'w')
    test_set = open(project_name + "/" + "test.csv", 'w')
    prop_dic = {}
    for iterator in range(depth):
        prop_dic[iterator] = []
    # Create a logger object
    logger = logging.getLogger()

    # Configure logger
    logging.basicConfig(filename=project_name + "/logfile.log",
                        format='%(filename)s: %(message)s', filemode='w')

    # Setting threshold level
    logger.setLevel(logging.WARNING)

    # Use the logging methods
    # logger.debug("This is a debug message")
    logger.info("This is a log file.")
    # logger.warning("This is a warning message")
    # logger.error("This is an error message")
    # logger.critical("This is a critical message")

    if multi:
        match = re.findall(r'([a-zA-Z]+)[,|\]]', label)
        for ontology in match:
            val = generate_url(ontology)
            url = val[0]
            about = (val[1])
            list_of_property_information = get_properties(url=url, project_name=project_name,
                                                        output_file="get_properties.csv", multi=multi)
            for property_line in list_of_property_information:
                count += 1
                prop = property_line.split(',')
                print("**************\n" + str(prop))
                template_generator(original_count=depth, prop_dic=prop_dic, test_set=test_set,
                                                    log=logger, output_file=output_file,
                                                    mother_ontology=about.strip().replace(
                                                        "http://dbpedia.org/ontology/",
                                                        "dbo:"), vessel=vessel,
                                                    project_name=project_name, prop=prop, suffix=" of <A> ?",
                                                    count=depth)

    else:

        val = generate_url(label)
        url = val[0]
        about = (val[1])

        list_of_property_information = get_properties(url=url, project_name=project_name,
                                                    output_file="get_properties.csv", multi=multi)

        for property_line in list_of_property_information:
            count += 1
            prop = property_line.split(',')
            print("**************\n"+str(prop))
            template_generator(original_count=depth, prop_dic=prop_dic, test_set=test_set, log=logger, output_file=output_file,
                                                mother_ontology=about.strip().replace("http://dbpedia.org/ontology/",
                                                                                        "dbo:"), vessel=vessel,
                                                project_name=project_name, prop=prop, suffix=" of <A> ?", count=depth)

    output_file.close()


if __name__ == "__main__":
    """
    Section to parse the command line arguments.
    """
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--label', dest='label', metavar='label',
                            help='label: person, place etc.', required=True)
    requiredNamed.add_argument(
        '--project_name', dest='project_name', metavar='project_name', help='test', required=True)
    requiredNamed.add_argument(
        '--depth', dest='depth', metavar='depth',
        help='Mention the depth you want to go in the knowledge graph (The number of questions will increase exponentially!), e.g. 2',
        required=False)
    requiredNamed.add_argument(
        '--multi', dest='multi', metavar='[Whether enable multi Ontologies]',
        help='Mention True/False you want to enable multi Ontologies, if you select True, you need to enter a list of ontologies for --label, e.g. --label \'[ontology1,ontology2,..]\'',
        required=False)
    args = parser.parse_args()
    label = args.label
    project_name = args.project_name
    depth = args.depth
    multi = args.multi
    generate_templates(label=label, project_name=project_name, depth=depth,
                    multi=multi)
    pass
