import pandas as pd
from pandas.core.internals.blocks import new_block
pd.set_option('display.max_columns', None)
import numpy as np
import argparse
import transformers
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, AutoTokenizer, BertModel, BertConfig, AutoModel, AdamW
from tqdm import tqdm
import wandb
import warnings
warnings.filterwarnings('ignore')
from utils import load_commonsense_data, load_qq_data, load_test_data

class CFG:
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    train_bs = 32
    test_bs = 1
    epochs = 10
    lr = 1e-5
    tokenizer = 'bert-base-uncased'

class Dataset(Dataset):
    def __init__(self, df, tokenizer, max_len, target_cols):
        self.df = df
        self.max_len = max_len
        self.text = df.text
        self.tokenizer = tokenizer
        self.targets = np.float32(df[target_cols].values)
        
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

def loss_fn(outputs, targets):
    return torch.nn.BCEWithLogitsLoss()(outputs, targets)

def train_fn(train_loader, model, optimizer, train_l):

    for epoch_num in range(CFG.epochs):

            train_loss = 0
            model.train()
            for _, data in enumerate(train_loader):
                ids = data['ids'].to(CFG.device, dtype = torch.long)
                mask = data['mask'].to(CFG.device, dtype = torch.long)
                token_type_ids = data['token_type_ids'].to(CFG.device, dtype = torch.long)
                targets = data['targets'].to(CFG.device, dtype = torch.float)

                outputs = model(ids, mask, token_type_ids)

                loss = loss_fn(outputs, targets)
                train_loss += loss
                
                loss.backward()
                optimizer.step()
                optimizer.zero_grad()
            
            print(
                f'Epochs: {epoch_num + 1} | Train Loss: {train_loss / len(train_loader): .3f}')

            empty_s = f'Epochs: {epoch_num + 1} | Train Loss: {train_loss / len(train_loader): .3f}'
            train_l.append(empty_s)
              
            wandb.log({f"epoch": epoch_num+1, 
                    f"train_loss": train_loss / len(train_loader)})

    return train_l

def test_fn(test_loader, model):
    
    model.eval()
    test_targets=[]
    test_outputs=[]
    with torch.no_grad():
        for data in test_loader:
            ids = data['ids'].to(CFG.device, dtype = torch.long)
            mask = data['mask'].to(CFG.device, dtype = torch.long)
            token_type_ids = data['token_type_ids'].to(CFG.device, dtype = torch.long)
            targets = data['targets'].to(CFG.device, dtype = torch.float)
            outputs = model(ids, mask, token_type_ids)
            test_targets.extend(targets.cpu().detach().numpy().tolist())
            test_outputs.extend(torch.sigmoid(outputs).cpu().detach().numpy().tolist())

    return test_outputs, test_targets

def save_model(model, dir):
    path = dir + "model.pth"
    torch.save(model.state_dict(), path)

def load_model(dir):
    path = dir + "model.pth"
    model = BERTModel()
    model.load_state_dict(torch.load(path))

    return model

def main(category, train, test):

    if category == 'commonsense':
        add = 'commonsense'
        target_cols = [col for col in train.columns if col not in ['Unnamed: 0', 'sent0', 'sent1', 'text']]
        test_target_cols = [col for col in test.columns if col not in ['Unnamed: 0', 'sent0', 'sent1', 'text']]
    else:
        add = 'qq'
        target_cols = [col for col in train.columns if col not in ['Unnamed: 0', 'id', 'qid1', 'qid2', 'question1', 'question2', 'text']]
        test_target_cols = [col for col in test.columns if col not in ['Unnamed: 0', '0', '1', '2', '3', '4', '5', '6', '7', '8', 'text']]

    dir = 'gsoc/saurav/Elimination/Model/' + add + '_bert/bert_'
    train_l = []

    wandb_config = {
      'model': add + '-classifier-bert'
    }

    run = wandb.init(project=add+'-classifier', 
                     name=wandb_config['model'],
                     config=wandb_config,
                     group=wandb_config['model'],
                     job_type="train",
                     anonymous=None)

    tokenizer = AutoTokenizer.from_pretrained(CFG.tokenizer)
    tokenizer.save_pretrained(dir+'tokenizer/')
    train_dataset = Dataset(train, tokenizer, CFG.max_len, target_cols)
    test_dataset = Dataset(test, tokenizer, CFG.max_len, test_target_cols)
    train_loader = DataLoader(train_dataset, batch_size=CFG.train_bs, 
                          num_workers=4, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=CFG.test_bs, 
                          num_workers=4, shuffle=False)
    model = BERTModel()
    model.to(CFG.device)
    optimizer = AdamW(params =  model.parameters(), lr=CFG.lr, weight_decay=1e-6)
    train_l = train_fn(train_loader, model, optimizer, [])

    # Save model
    save_model(model, dir)
    wandb.finish()

    # Test Accuracy
    loaded_model = load_model(dir)
    loaded_model.to(CFG.device)
    a, b = test_fn(test_loader, loaded_model)
    acc = 0
    for x, y in zip(a, b):
      l1 = [0 if x[0] < 0.5 else 1]
      l2 = [0 if y[0] < 0.5 else 1]
      if l1 == l2:
        acc += 1
    print('Test Accuracy: ', (acc/len(a)*100))
    acc = (acc/len(a)*100)
    train_l.append(f'Test Accuracy: {acc}')

    filelog = open(dir+'training_log.txt', 'w', encoding="utf8")
    filelog.writelines(train_l)
    filelog.close()

    
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--category', dest='category', metavar='category',
                               help='category', required=True)
    requiredNamed.add_argument('--train_path', dest='train_path', metavar='train path',
                               help='train path', required=True)
    requiredNamed.add_argument('--test_path', dest='test_path', metavar='test path',
                               help='test path', required=True)

    args = parser.parse_args()
    category = args.category
    train_path = args.train_path
    test_path = args.test_path
    if category == 'commonsense':
        data = load_commonsense_data(train_path)
    else:
        data = load_qq_data(train_path)
    train = data[:40000] # many dataset size were tested 
    # Test data - same for both commonsense and quora question pairs dataset
    test = load_test_data(test_path)
    # print(train.shape, test.shape)
    # print(train.columns)
    # print(train.head())

    # Setting max len
    max_len = 0
    for row in train.iterrows():
        try:
            max_len = max(max_len, len(row[1]['text'].split()))
        except:
            pass
    CFG.max_len = max_len + 10

    main(category, train, test)
