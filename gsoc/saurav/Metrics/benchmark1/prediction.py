"""
Receives qald_nlq file and outputs sparql prediction from the model
"""

import argparse
import os
import sys
from tqdm import tqdm
sys.path.append(os.getcwd()+'/nspm')
from interpreter import interpret

def read(input_file):
    
    file = open(input_file, 'r', encoding="utf8")
    Lines = file.readlines()
    data = []
    for i in range(len(Lines)):
        data.append(Lines[i].replace('\n', " "))

    file.close()
    return data

def write_sparql(data):
    output_file = open("gsoc/saurav/Metrics/benchmark1/sparql_prediction_file", 'w')
    for sub_data in data:
        output_file.write(sub_data+'\n')

def predict(qald_nlq, model_dir):
    nlq_data = read(qald_nlq)
    sparql_output = interpret(model_dir, nlq_data)

    return sparql_output


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  requiredNamed = parser.add_argument_group('required named arguments')
  requiredNamed.add_argument('--qald_nlq', dest='qald_nlq', metavar='qald_nlq',
                        help='qald nlq', required=True)
  requiredNamed.add_argument(
      '--model_dir', dest='model_dir', metavar='model_dir', help='model directory', required=True)

  args = parser.parse_args()
  qald_nlq = args.qald_nlq
  model_dir = args.model_dir

  final_data = predict(qald_nlq=qald_nlq, model_dir=model_dir)
  write_sparql(final_data)
