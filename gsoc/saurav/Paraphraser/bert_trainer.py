import pandas as pd
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

class CFG:
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    train_bs = 64
    val_bs = 64
    test_bs = 64
    epochs = 25
    lr = 3e-5
    tokenizer = 'bert-base-uncased'

class Dataset(Dataset):
    def __init__(self, df, tokenizer, max_len, target_cols):
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
        self.fc = torch.nn.Linear(768,3)
    
    def forward(self, ids, mask, token_type_ids):
        _, features = self.bert(ids, attention_mask = mask, token_type_ids = token_type_ids, return_dict=False)
        output = self.fc(features)
        return output


def load_data(file_path):
    data = pd.read_csv(file_path, sep = ";", names = ['original','paraphrase', 'value'])
    data['text'] = data['original'] + '[SEP]' + data['paraphrase']
    f,s,t = [], [], []
    for row in data.iterrows():
        if row[1]['value'] == -1:
            f.append(1)
            s.append(0)
            t.append(0)
        elif row[1]['value'] == 0:
            f.append(0)
            s.append(1)
            t.append(0)
        elif row[1]['value'] == 1:
            f.append(0)
            s.append(0)
            t.append(1)

    data['-1'] = f
    data['0'] = s
    data['1'] = t

    return data

def loss_fn(outputs, targets):
    return torch.nn.BCEWithLogitsLoss()(outputs, targets)

def train_fn(train_loader, val_loader, model, optimizer, train_l):

    for epoch_num in range(CFG.epochs):

            train_loss = 0
            val_loss = 0

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

            model.eval()
            with torch.no_grad():
                for _, data in enumerate(train_loader):
                    ids = data['ids'].to(CFG.device, dtype = torch.long)
                    mask = data['mask'].to(CFG.device, dtype = torch.long)
                    token_type_ids = data['token_type_ids'].to(CFG.device, dtype = torch.long)
                    targets = data['targets'].to(CFG.device, dtype = torch.float)

                    outputs = model(ids, mask, token_type_ids)

                    loss = loss_fn(outputs, targets)
                    val_loss += loss
            
            print(
                f'Epochs: {epoch_num + 1} | Train Loss: {train_loss / len(train_loader): .3f} \
                | Val Loss: {val_loss / len(val_loader): .3f}')

            empty_s = f'Epochs: {epoch_num + 1} | Train Loss: {train_loss / len(train_loader): .3f} \
                | Val Loss: {val_loss / len(val_loader): .3f}\n'
            train_l.append(empty_s)
              
            wandb.log({f"epoch": epoch_num+1, 
                    f"train_loss": train_loss / len(train_loader), 
                    f"val_loss": val_loss / len(val_loader)})

    return train_l

def test_fn(test_loader, model):
    
    model.eval()
    test_targets=[]
    test_outputs=[]
    with torch.no_grad():
        for _, data in enumerate(test_loader):
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

def main(train, val, test):

    dir = 'gsoc/saurav/Paraphraser/Model/bert/bert_'
    train_l = []

    wandb_config = {
      'model': 'para-classifier-bert'
    }

    run = wandb.init(project='para-classifier', 
                     name=wandb_config['model'],
                     config=wandb_config,
                     group=wandb_config['model'],
                     job_type="train",
                     anonymous=None)

    target_cols = [col for col in train.columns if col not in ['index', 'original', 'paraphrase', 'value', 'text']]
    tokenizer = AutoTokenizer.from_pretrained(CFG.tokenizer)
    tokenizer.save_pretrained(dir+'tokenizer/')
    train_dataset = Dataset(train, tokenizer, CFG.max_len, target_cols)
    val_dataset = Dataset(val, tokenizer, CFG.max_len, target_cols)
    test_dataset = Dataset(test, tokenizer, CFG.max_len, target_cols)
    train_loader = DataLoader(train_dataset, batch_size=CFG.train_bs, 
                          num_workers=4, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=CFG.val_bs, 
                          num_workers=4, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=CFG.test_bs, 
                          num_workers=4, shuffle=False)
    model = BERTModel()
    model.to(CFG.device)
    optimizer = AdamW(params =  model.parameters(), lr=CFG.lr, weight_decay=1e-6)
    train_l = train_fn(train_loader, val_loader, model, optimizer, [])

    # Save model
    save_model(model, dir)
    wandb.finish()

    # Test Accuracy
    loaded_model = load_model(dir)
    loaded_model.to(CFG.device)
    a, b = test_fn(test_loader, loaded_model)
    acc = 0
    for x, y in zip(a, b):
      l1 = np.argmax(x)
      l2 = np.argmax(y)
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

    requiredNamed.add_argument('--file_path', dest='file_path', metavar='file path',
                               help='file path', required=True)

    args = parser.parse_args()
    file_path = args.file_path
    data = load_data(file_path)
    print(data.shape)

    # Setting max len
    max_len = 0
    for row in data.iterrows():
        max_len = max(max_len, len(row[1]['text'].split()))
    CFG.max_len = max_len + 10

    train, val, test = np.split(data.sample(frac=1, random_state=42), [int(.8*len(data)), int(.9*len(data))])
    train = train.reset_index()
    val = val.reset_index()
    test = test.reset_index()
    # print(data.shape, train.shape, val.shape, test.shape)
    # print(train.head())
    main(train, val, test)
