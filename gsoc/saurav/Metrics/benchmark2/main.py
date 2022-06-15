"""
Calculates the bleu score between the true sparql queries and 
model's predicted sparql queries.
"""

import argparse
import sys
import os
sys.path.append(os.getcwd()+'/gsoc/saurav/Metrics/measures')
from bleu import bleu

def read(input_file1, input_file2):
    file1 = open(input_file1, 'r', encoding="utf8")
    Lines1 = file1.readlines()
    file2 = open(input_file2, 'r', encoding="utf8")
    Lines2 = file2.readlines()
    target = []
    predicted = []
    for i in range(len(Lines1)):
        target.append(Lines1[i].replace('\n', " "))
    for i in range(len(Lines2)):
        predicted.append(Lines2[i].replace('\n', " "))

    file1.close()
    file2.close()

    return target, predicted

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument(
        '--true_file', dest='true_file', metavar='true_file', help='truefile', required=True)
    requiredNamed.add_argument(
        '--prediction_file', dest='prediction_file', metavar='prediction_file', help='prediction file', required=True)
    args = parser.parse_args()
    true_file = args.true_file
    prediction_file = args.prediction_file

    target, predicted = read(true_file, prediction_file)
    bleu(target, predicted)
    