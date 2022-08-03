import shutil
import torch
import os
import re
import pandas as pd
import transformers
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, AutoTokenizer, BertModel, BertConfig, AutoModel, AdamW
from tqdm import tqdm
import wandb
import warnings
warnings.filterwarnings('ignore')

def read(input_file):
    file1 = open(input_file, 'r', encoding="utf8")
    Lines1 = file1.readlines()
    data = []
    for i in range(len(Lines1)):
        data.append(Lines1[i].replace('\n', " "))

    file1.close()
    return data

def write_data(output_file, data):

    output_file = open(output_file, 'w')
    for sub_data in data:
        output_file.write(sub_data+'\n')

def write_final_data(output_file, data):

    output_file = open(output_file, 'w')
    for sub_data in data:
        sub_data = ';'.join(sub_data)
        output_file.write(sub_data+'\n')

def load_model(dir):
    path = dir + "model.pth"
    model = BERTModel()
    model.load_state_dict(torch.load(path))
    tokenizer = AutoTokenizer.from_pretrained(dir+'tokenizer/')

    return model, tokenizer

def load_commonsense_data(file_path):
    df = pd.DataFrame(columns=['sent0', 'sent1', 'value'])
    data = read(file_path)
    for sub_data in data:
        split = sub_data.split(';')
        if len(split) == 3:
            df.loc[len(df)] = [split[0], split[1], int(split[2].strip())]
    
    df['text'] = df['sent0'] + '[SEP]' + df['sent1']

    return df

def load_qq_data(file_path):
    df = pd.read_csv(file_path)
    df['text'] = df['question1'] + '[SEP]' + df['question2']

    return df

def load_test_data(file_path):
    df = pd.DataFrame(columns=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    data = read(file_path)
    for sub_data in data:
        split = sub_data.split(';')
        if len(split) == 10:
            df.loc[len(df)] = [split[0], split[1], split[2], split[3], split[4], split[5], split[6], split[7], split[8], int(split[9].strip())]
    
    df['text'] = df['1'] + '[SEP]' + df['2']

    return df

class Dataset(Dataset):
    def __init__(self, df, tokenizer, max_len, target_cols=None):
        self.df = df
        self.max_len = max_len
        self.text = df.text
        self.tokenizer = tokenizer
        self.targets = df[target_cols].values
        
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, index):
        text = self.text[index]
        inputs = self.tokenizer.encode_plus(
            text,
            truncation=True,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            return_token_type_ids=True
        )
        ids = inputs['input_ids']
        mask = inputs['attention_mask']
        token_type_ids = inputs["token_type_ids"]
        
        return {
            'ids': torch.tensor(ids, dtype=torch.long),
            'mask': torch.tensor(mask, dtype=torch.long),
            'token_type_ids': torch.tensor(token_type_ids, dtype=torch.long),
            'targets': torch.tensor(self.targets[index], dtype=torch.float)
        }

class BERTModel(torch.nn.Module):
    def __init__(self):
        super(BERTModel, self).__init__()
        self.bert = AutoModel.from_pretrained('bert-base-uncased')
        self.fc = torch.nn.Linear(768,1)
    
    def forward(self, ids, mask, token_type_ids):
        _, features = self.bert(ids, attention_mask = mask, token_type_ids = token_type_ids, return_dict=False)
        output = self.fc(features)
        return output