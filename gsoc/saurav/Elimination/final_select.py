import argparse
import torch
import pandas as pd
from tqdm import tqdm
from utils import read, write_final_data, load_model
from classifier import predict

def final_select(data, elimination=False, elimination_type="", model_file1="", model_file2=""):

    final_data = []
    template_set = set()
    if elimination == "True":
        model, tokenizer = load_model(model_file1) 
        print(model_file2)
        if model_file2 != None:
            model2, tokenizer2 = load_model(model_file2) 
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    for sub_data in tqdm(data):
        sub_split = sub_data.split(';')
        template1 = sub_split[1]
        template2 = sub_split[2]

        if elimination == "False":

            rem = [sub_split[0], '', '', sub_split[3], sub_split[4]]
            copy = rem.copy()
            copy2 = rem.copy()
            copy.insert(3, template1)
            copy.append('Original')
            copy2.insert(3, template2)
            copy2.append('Paraphrased')
            if template1 not in template_set:
                final_data.append(copy)
                template_set.add(template1)
            if template2 not in template_set:
                final_data.append(copy2)
                template_set.add(template2)

        else:

            df = pd.DataFrame(columns=['1', '2'])
            df.loc[len(df)] = [template1, template2]
            output = predict(device, df, model, tokenizer)
            output = [0 if output[0][0] < 0.5 else 1][0]
            if model_file2 != None:
                output2 = predict(device, df, model2, tokenizer2)
                output2 = [0 if output2[0][0] < 0.5 else 1][0]
            rem = [sub_split[0], '', '', sub_split[3], sub_split[4]]
            copy = rem.copy()
            copy2 = rem.copy()
            copy.insert(3, template1)
            copy.append('Original')
            copy2.insert(3, template2)
            copy2.append('Paraphrased')
            if elimination_type == 'commonsense': # commonsense
                if output == 0 and template2 not in template_set: # refined against commonsense hence add paraphrase
                    final_data.append(copy2)
                    template_set.add(template2)
                elif output == 1 and template1 not in template_set: # paraphrase against commonsense hence add refined
                    final_data.append(copy)
                    template_set.add(template1)
            elif elimination_type == 'qq': # qq
                if output == 0 and template1 not in template_set:
                    final_data.append(copy)
                    template_set.add(template1)
                elif output == 1 and template2 not in template_set: # is duplicate
                    final_data.append(copy2)
                    template_set.add(template2)
            else: # ensemble
                if output == 1 and output2 == 0: # add refined as both the methods are predicting refined
                    if template1 not in template_set:
                        final_data.append(copy)
                        template_set.add(template1)
                else:
                    if template2 not in template_set:
                        final_data.append(copy2)
                        template_set.add(template2)

    return final_data
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--input_file', dest='input_file', metavar='input_file',
                               help='input_file', required=True)
    requiredNamed.add_argument('--output_file', dest='output_file', metavar='output_file',
                               help='output_file', required=True)
    requiredNamed.add_argument('--elimination', dest='elimination', metavar='elimination',
                               help='elimination', required=True)
    requiredNamed.add_argument('--elimination_type', dest='elimination_type', metavar='elimination_type',
                               help='elimination_type', required=False)
    requiredNamed.add_argument('--model_file1', dest='model_file1', metavar='model_file1',
                               help='model_file1', required=False)
    requiredNamed.add_argument('--model_file2', dest='model_file2', metavar='model_file2',
                               help='model_file2', required=False)

    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file
    elimination = args.elimination
    elimination_type = args.elimination_type
    model_file1 = args.model_file1
    model_file2 = args.model_file2

    data = read(input_file)
    final_data = final_select(data, elimination, elimination_type, model_file1, model_file2)
    print('Size: ', len(final_data))
    write_final_data(output_file, final_data)
