import argparse
import json
from tqdm import tqdm
from interpreter import interprete
from extract_questions import read_json, write_to_ask
from retrieve_answers import read_sparqls, retrieve
from reconstruct_json import construct_json



def benchmark(trained_model, test_set, answer_file="answers.json"):
    # Deconstruct the questions and infos from test set
    questions_info, questions = read_json(test_set)

    # Write the questions to to_ask.txt
    write_to_ask(questions)

    # Use Interpreter to interprete them into decoded queries stored in output_decoded.txt
    interprete(trained_model)

    # Use the sparql endpoint (http://dbpedia.org/sparql) to retrieve answers of the queries
    sparqls = read_sparqls()
    answers = []
    print("Retrieving answers of queries via SPARQL endpoint")
    for query in tqdm(sparqls):
        try:
            answer_group = retrieve(query)
        except:
            answer_group = []
        answers.append(answer_group)

    json_file = construct_json("qald-9-train-multilingual", questions_info, questions, sparqls, answers)
    path = "../gsoc/zheyuan/utility/benchmark/"
    with open(path+"answers.qald.json", "w") as f:
        # js = json.dumps(json_file, indent=4, separators=(',', ':'))
        json.dump(json_file, f)



if __name__ == "__main__":
    """
    Section to parse the command line arguments.
    """
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--model', dest='model', metavar='[modelId]',
                               help='the trained model', required=True)
    requiredNamed.add_argument('--test', dest='test', metavar='[testset file name]',
                               help='the testing qald set file name', required=True)
    requiredNamed.add_argument('--answer', dest='answer', metavar='[answer file name]',
                              help='the answers of qald dataset file name', required=False)
    args = parser.parse_args()
    trained_model = args.model
    test_set = args.test
    answer_file = args.answer
    benchmark(trained_model,test_set, answer_file)
    pass