"""
Parses the qald-9-train-multilingual.json file and generates qald_true.json 
file with the answers, and qald_nlq with the questions.
"""

import json
import argparse


def process_answers(ans):
    rsc = ans.split('/')[-1]
    return rsc

def read(qald_file):
    f = open(qald_file)
    data  = json.load(f)['questions']
    ids = []
    questions = []
    sparql = []
    answers = []
    for sub_data in data:

        # Fetching ids
        ids.append(sub_data['id'])

        # Fetching english nlq
        for q in sub_data['question']:
            if q['language'] == 'en':
                questions.append(q['string'])

        # Fetching sparql query
        sparql.append(sub_data['query']['sparql'])

        # Fetching answers
        if sub_data['answertype'] == 'boolean':
            answers.append({"answers": [{"resource": str(sub_data['answers'][0]['boolean'])}]})
        else:
            answer = []
            for a in sub_data['answers'][0]['results']['bindings']:
                for key, val in a.items():
                    rsc = process_answers(val['value'])
                    answer.append({"resource": rsc})

            answers.append({"answers": answer})

    return answers, questions

def write_answers(data):
    with open("gsoc/saurav/Metrics/benchmark1/qald_true.json", "w") as w:
        json.dump(data, w, ensure_ascii = False)

def write_nlq(data):
    output_file = open("gsoc/saurav/Metrics/benchmark1/qald_nlq", 'w')
    for sub_data in data:
        output_file.write(sub_data+'\n')

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument(
        '--qald_file', dest='qald_file', metavar='qald_file', help='qald file', required=True)
    args = parser.parse_args()
    qald_file = args.qald_file

    answers, questions = read(qald_file)
    write_answers(answers)
    write_nlq(questions)
