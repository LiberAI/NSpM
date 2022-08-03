import argparse
import pandas as pd
import os
import sys
from tqdm import tqdm
sys.path.append(os.getcwd()+'/gsoc/saurav/Paraphraser')
from paraphrase_questions import paraphrase_questions, prepare_model, pick_final_sentence
from bert_utils import read

def expand_data(file_name):

    data = pd.read_csv(file_name)
    # paraphraser model
    tokenizer, device, model = prepare_model()
    final_data = []
    for i, row in tqdm(data.iterrows()):
        s1 = row['sent0']
        s2 = row['sent1']
        s1_candidates = paraphrase_questions(tokenizer, device, model, s1)
        s2_candidates = paraphrase_questions(tokenizer, device, model, s2)
        s1_best_candidate = pick_final_sentence(s1, s1_candidates)
        s2_best_candidate = pick_final_sentence(s2, s2_candidates)

        # combinations to expand the dataset
        final_data.append([s1, s2])
        final_data.append([s1, s2_best_candidate])
        final_data.append([s1_best_candidate, s2])
        final_data.append([s1_best_candidate, s2_best_candidate])

    return final_data

def expand_answers(file_name):

    data = pd.read_csv(file_name, header=None)
    final_data = []
    for i, row in tqdm(data.iterrows()):
        final_data.append(row.values[1])
        final_data.append(row.values[1])
        final_data.append(row.values[1])
        final_data.append(row.values[1])
        
    return final_data

def write_data(output_file, data):

    output_file = open(output_file, 'w')
    for sub_data in data:
        try:
            sub_data = ';'.join(sub_data)
            output_file.write(sub_data+'\n')
        except:
            output_file.write(str(sub_data)+'\n')

def eliminate_data(file1, file2):

    train_data = read(file1)
    train_answers = read(file2)
    final_data = []
    for x, y in zip(train_data, train_answers):
        s = x.split(';')
        s1, s2 = s[0].strip(), s[1].strip()
        if s1 == '' or s2 == '':
            pass
        else:
            final_data.append([s1, s2, y])

    return final_data

if __name__ == "__main__":
    """
    Section to parse the command line arguments.
    """
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--input_dir', dest='input_dir', metavar='input_dir',
                            help='input_dir', required=True)
    requiredNamed.add_argument('--output_dir', dest='output_dir', metavar='output_dir',
                            help='output_dir', required=True)

    args = parser.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    train_data1 = expand_data(input_dir+'/subtaskA_data_all.csv')
    train_data2 = expand_answers(input_dir+'/subtaskA_answers_all.csv')
    write_data(output_dir+'/train_data', train_data1)
    write_data(output_dir+'/train_answers', train_data2)

    final_data = eliminate_data(output_dir+'/train_data', output_dir+'/train_answers')
    write_data(output_dir+'/combined_train_data', final_data)    
