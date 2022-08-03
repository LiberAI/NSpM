import argparse
import torch 
import pandas as pd
import numpy as np
from utils import BERTModel, Dataset, load_model, read, load_test_data

def encode(test_set, tokenizer, device):
    input_ids = []
    attention_masks = []
    token_type_ids = []
    for _, sent in test_set.iterrows():
        input_sent = sent['1'] + '[SEP]' + sent['2']
        encoded_dict = tokenizer.encode_plus(
            input_sent,  # Sentence to encode.
            add_special_tokens=True,  # Add '[CLS]' and '[SEP]'
            max_length=64,  # Pad & truncate all sentences.
            truncation=True,
            pad_to_max_length=True,
            return_attention_mask=True,  # Construct attn. masks.
            return_tensors='pt',  # Return pytorch tensors.
        )
        input_ids.append(encoded_dict['input_ids'].to(device))
        # And its attention mask (simply differentiates padding from non-padding).
        attention_masks.append(encoded_dict['attention_mask'].to(device))
        token_type_ids.append(encoded_dict['token_type_ids'].to(device))

    input_ids = torch.cat(input_ids, dim=0)
    attention_masks = torch.cat(attention_masks, dim=0)
    token_type_ids = torch.cat(token_type_ids, dim=0)
    return input_ids, attention_masks, token_type_ids

def predict(device, testset, model, tokenizer):

    ids, mask, token_type_ids = encode(testset, tokenizer, device)
    model.to(device)
    model.eval()
    test_outputs=[]
    with torch.no_grad():
        for num in range(len(testset)):
            input_ids = ids[num].unsqueeze(0).to(device, dtype = torch.long)
            attention_mask = mask[num].unsqueeze(0).to(device, dtype = torch.long)
            token_ids = token_type_ids[num].unsqueeze(0).to(device, dtype = torch.long)
            outputs = model(input_ids, attention_mask, token_ids)
            test_outputs.extend(torch.sigmoid(outputs).cpu().detach().numpy().tolist())

    return test_outputs
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--category', dest='category', metavar='category',
                               help='category', required=True)
    requiredNamed.add_argument('--test_file', dest='test_file', metavar='test_file',
                               help='test_file', required=True)
    requiredNamed.add_argument('--model_file', dest='model_file', metavar='model_file',
                               help='Bert fine-tuned model\'s folder path', required=True)

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    args = parser.parse_args()
    category = args.category
    test_file = args.test_file
    model_file = args.model_file

    testset = load_test_data(test_file)

    model, tokenizer = load_model(model_file)   

    output = predict(device, testset, model, tokenizer)
    acc = 0
    for i, j in zip(output, testset.iterrows()):
      x = [0 if i[0] < 0.5 else 1]
      print(j[1]['1'], j[1]['2'], j[1]['9'], x[0])
      if x[0] == j[1]['9']:
        acc+=1

    print('Test Accuracy: ', (acc/len(testset)*100))
