# !pip install transformers
# !pip install sentence-transformers

from sentence_transformers import SentenceTransformer, util
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer
import numpy as np
import argparse
from tqdm import tqdm
import re
import torch.nn.functional as F

def read(input_file):
    
    file = open(input_file, 'r', encoding="utf8")
    Lines = file.readlines()
    data = []
    for i in range(len(Lines)):
        data.append(Lines[i].replace('\n', " "))

    file.close()

    return data

def write_score_data(output_file, data):

    output_file = open(output_file, 'w')
    for sub_data in data:
        sub_data[-1] = str(sub_data[-1])
        sub_data = ';'.join(sub_data) + '\n'
        output_file.write(sub_data)

def sort_score(data):

    sorted_data = sorted(data, key=lambda x: x[-1], reverse=True)
    return sorted_data

def semantic_similarity(model, s1, s2):

    sentence1 = s1
    sentence2 = s2
    # encode sentences to get their embeddings
    embedding1 = model.encode(sentence1, convert_to_tensor=True)
    embedding2 = model.encode(sentence2, convert_to_tensor=True)

    # compute similarity scores of two embeddings
    cosine_scores = F.cosine_similarity(embedding1, embedding2, dim=0)
    
    return cosine_scores.item()


def eliminate(input_file, output_dir, threshold):

    model = SentenceTransformer('stsb-roberta-large')
    data = read(input_file)
    score_data = []
    for sub_data in tqdm(data):
        split_data = sub_data.split(';')
        ontology = split_data[0]
        og = split_data[1]
        para = split_data[2]
        score = semantic_similarity(model, og, para)
        if score >= threshold:
            split_data.append(score)
            score_data.append(split_data)

    sorted_data = sort_score(score_data)
    write_score_data(output_dir+"/score_data", sorted_data)

if __name__ == "__main__":
    """
    Section to parse the command line arguments.
    """
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--input_file', dest='input_file', metavar='input_file',
                            help='input_file', required=True)
    requiredNamed.add_argument('--output_dir', dest='output_dir', metavar='output_dir',
                            help='output_dir', required=True)
    requiredNamed.add_argument('--threshold', dest='threshold', metavar='threshold',
                            help='threshold', required=True)

    args = parser.parse_args()
    input_file = args.input_file
    output_dir = args.output_dir
    threshold = float(args.threshold)
    eliminate(input_file=input_file, output_dir=output_dir, threshold=threshold)