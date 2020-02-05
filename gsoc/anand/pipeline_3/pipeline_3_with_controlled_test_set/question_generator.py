import json
import argparse

def question_generator(query):
   pass 



if __name__ == "__main__":
    """
    Section to parse the command line arguments.
    """
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--url', dest='url', metavar='url',
                                                            help='Webpage URL: eg-http://mappings.dbpedia.org/server/ontology/classes/Place', required=True)
    requiredNamed.add_argument(
        '--output_file', dest='out_put', metavar='out_put', help='temp.csv', required=True)
    requiredNamed.add_argument(
        '--project_name', dest='project_name', metavar='project_name', help='test', required=True)
    args = parser.parse_args()
    url = args.url
    output_file = args.out_put
    project_name = args.project_name
    pass