"""
Calculates the f1 score between qald answers and model's predicted 
answers.
"""

import json
import sys
import os
import argparse
import numpy as np
sys.path.append(os.getcwd()+'/gsoc/saurav/Metrics/measures')
from f1score import f1score

def read(input_file1, input_file2):
    file1 = open(input_file1)
    Lines1 = json.load(file1)
    file2 = open(input_file2)
    Lines2 = json.load(file2)
    target = []
    predicted = []
    for sub_line in Lines1:
        sub_list = []
        for data in sub_line['answers']:
            sub_list.append(data['resource'])
        target.append(sub_list)
    for sub_line in Lines2:
        sub_list = []
        for data in sub_line['answers']:
            sub_list.append(data['resource'])
        predicted.append(sub_list)

    file1.close()
    file2.close()

    return target, predicted

if __name__ == "__main__":
    """
    Section to parse the command line arguments.
    """
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--true_file', dest='true_file', metavar='true_file',
                            help='true file', required=True)
    requiredNamed.add_argument('--prediction_file', dest='prediction_file', metavar='prediction_file', 
                            help='prediction file', required=True)
    args = parser.parse_args()
    true_file = args.true_file
    prediction_file = args.prediction_file
    target, predicted = read(true_file, prediction_file)

    f1_score = []
    for i in range(min(len(target), len(predicted))):
        score = f1score(target[i], predicted[i])
        f1_score.append(score)

    f1_score = np.mean(f1_score)
    print("F1 score: ", f1_score)
    