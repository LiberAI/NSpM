import shutil
import torch
import os
import re
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


def load_model(dir):
    path = dir + "model.pth"
    model = BERTModel()
    model.load_state_dict(torch.load(path))
    tokenizer = AutoTokenizer.from_pretrained(dir+'tokenizer/')

    return model, tokenizer

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
        self.bert = AutoModel.from_pretrained('albert-base-v2')
        self.fc = torch.nn.Linear(768,3)
    
    def forward(self, ids, mask, token_type_ids):
        _, features = self.bert(ids, attention_mask = mask, token_type_ids = token_type_ids, return_dict=False)
        output = self.fc(features)
        return output