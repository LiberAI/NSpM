import argparse
import torch 
import pandas as pd
import numpy as np
from bert_utils import BERTModel, Dataset, load_model, read

def encode(test_set, tokenizer, device):
    input_ids = []
    attention_masks = []
    token_type_ids = []
    for sent in test_set:
        input_sent = sent[0] + '[SEP]' + sent[1]
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

    final_output = []
    for output in test_outputs:
        val = np.argmax(output)
        if val == 0:
            final_output.append(-1)
        elif val == 1:
            final_output.append(0)
        else:
            final_output.append(1)

    return final_output
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--model', dest='model', metavar='model folder',
                               help='Bert fine-tuned model\'s folder path', required=False)

    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    testset = [['When is the birth date of <A> ?', 'When is the birthday of <A> ?'],
               ["When is the birth date of <A> ?", "When was <A> born ?"],
               ["When is the birth date of <A> ?", "Where does <A> come from ?"],
               ["When is the birth date of <A> ?","What is the birth name of <A> ?"],
               ["How many child did <A> have ?","How many children did <A> have ?"]]

    model, tokenizer = load_model('gsoc/saurav/Paraphraser/Model/albert-base-v2/albert-base-v2/albert-base-v2_')   

    output = predict(device, testset, model, tokenizer)
    for i in output:
      print(i)
