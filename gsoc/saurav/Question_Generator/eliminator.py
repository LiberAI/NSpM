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

def write_results(output_file, data):

    for sub_data in data:
        sub_data = ';'.join(sub_data) + '\n'
        output_file.write(sub_data)

def write_score_data(output_file, data):

    output_file = open(output_file, 'w')
    for sub_data in data:
        sub_data[2] = str(sub_data[2])
        sub_data = ';'.join(sub_data) + '\n'
        output_file.write(sub_data)

def sort_score(data):
    
    sorted_data = sorted(data, key=lambda x: x[2], reverse=True)
    return sorted_data

def remove_text(question, p):
    
    simple_flag = 1
    try:
        p_first = p.split()[0]
        q_list = question.split()
        p_first_index = q_list.index(p_first)
        if q_list[p_first_index-2] != "is":
            simple_flag = 0
    except:
        pass

    return simple_flag

def remove_bracket(question):

    r = re.compile(r'\([^)]*\)')
    r = re.sub(r, '', question)
    r = r.replace("  ", " ")
    return r

def lemmatize(word):

    lemmatizer = WordNetLemmatizer()
    base = lemmatizer.lemmatize(word)
    return base

def split_property_check(question, p):

    ok = 1
    p_split = p.split()
    for word in p_split:
        base = lemmatize(word)
        if word not in question and base not in question:
            ok = 0
    
    return ok

# complete property string check i.e 2/3 words together
def complete_property_check(question, p1, p2):

    ok = 1
    if p1 not in question:
        ok = 0
    if p2 not in question:
        ok = 0

    return ok

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
    output_file = open(output_dir+"/final_template_generator", 'w')
    data = read(input_file)
    final_data = []
    score_data = []
    for sub_data in tqdm(data):
        sub_data = sub_data.split(';')
        original_question = sub_data[3]
        question = sub_data[-4]
        p1 = sub_data[-3]
        p2 = sub_data[-2]
        score = semantic_similarity(model, p1, p2)
        ok = complete_property_check(question, p1, p2)
        score_data.append([p1, p2, score])


        # split property check
        if ok == 0:
            ok1 = split_property_check(question, p1)
            ok2 = split_property_check(question, p2)
            ok = ok1 & ok2

        # Cases where Qgen adds unnecessary terms in the
        # transformed question. Mostly in simple questions
        simple_flag = 1
        if p1 == p2:
            simple_flag = remove_text(question, p1)
        if not simple_flag:
            ok = 0

        new_data = []
        if score >= threshold:
            if ok:
                for i in range(6):
                    new_data.append(sub_data[i])
                new_data.append(sub_data[7])
                new_data.append(sub_data[8])
                question = question.replace("ABC", "<A>")
                # adding space between char and ?
                if question[-2] != ' ':
                    question = question[:-1]
                    question += " ?"
                question = remove_bracket(question)
                new_data[3] = question
                p1 = remove_bracket(p1)
                new_data[-2] = p1
                p2 = remove_bracket(p2)
                new_data[-1] = p2
                if question != original_question:
                    new_data.append('QGen')
                else:
                    new_data.append('Original')
                final_data.append(new_data)
            else:
                for i in range(6):
                    val = sub_data[i]
                    if i == 3:
                        val = remove_bracket(val)
                    new_data.append(val)
                new_data.append(remove_bracket(sub_data[7]))
                new_data.append(remove_bracket(sub_data[8]))
                new_data.append('Original')
                final_data.append(new_data)

    write_results(output_file, final_data)
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
