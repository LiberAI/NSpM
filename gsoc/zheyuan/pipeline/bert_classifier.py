import argparse
import torch #version==1.6.0
from transformers import BertTokenizer
from transformers import BertForSequenceClassification
import numpy as np



def load_model(model_dir, device):
    model = BertForSequenceClassification.from_pretrained(model_dir)
    tokenizer = BertTokenizer.from_pretrained(model_dir)

    # Copy the model to the GPU.
    model.to(device)
    return model, tokenizer

def encode(test_set, tokenizer):
    input_ids = []
    attention_masks = []
    for sent in test_set[:10]:
        encoded_dict = tokenizer.encode_plus(
            sent[0],
            sent[1],  # Sentence to encode.
            add_special_tokens=True,  # Add '[CLS]' and '[SEP]'
            max_length=64,  # Pad & truncate all sentences.
            truncation=True,
            pad_to_max_length=True,
            return_attention_mask=True,  # Construct attn. masks.
            return_tensors='pt',  # Return pytorch tensors.
        )
        input_ids.append(encoded_dict['input_ids'])

        # And its attention mask (simply differentiates padding from non-padding).
        attention_masks.append(encoded_dict['attention_mask'])
    input_ids = torch.cat(input_ids, dim=0)
    attention_masks = torch.cat(attention_masks, dim=0)
    return input_ids, attention_masks

def predict(device, test_set, model, tokenizer):
    input_ids, attention_masks = encode(test_set, tokenizer)
    model.eval()
    # Tracking variables
    predictions = []
    # Add batch to GPU
    b_input_ids = input_ids.to(device)
    b_input_mask = attention_masks.to(device)
    # Telling the model not to compute or store gradients, saving memory and
    # speeding up prediction
    with torch.no_grad():
        # Forward pass, calculate logit predictions
        outputs = model(b_input_ids, token_type_ids=None,
                        attention_mask=b_input_mask)
    logits = outputs[0]
    # Move logits and labels to CPU
    logits = logits.detach().cpu().numpy()
    # Store predictions and true labels
    predictions.append(logits)
    pred_labels = []
    print(predictions)
    for i in range(len(predictions[0])):
        # get the highest score of logits to be the class
        # the result will be 0,1,2 so it should be -1
        pred_labels.append(np.argmax(predictions[0][i]).flatten()[0]-1)
    return pred_labels

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--model', dest='model', metavar='model folder',
                               help='Bert fine-tuned model\'s folder path', required=True)
    # requiredNamed.add_argument('--testset', dest='testset', metavar='testset',
    #                            help='A list: [[Origin, Paraphrase1],[O, P2]..]', required=True)


    # If there's a GPU available...
    if torch.cuda.is_available():

        # Tell PyTorch to use the GPU.
        device = torch.device("cuda")

        print('There are %d GPU(s) available.' % torch.cuda.device_count())

        print('We will use the GPU:', torch.cuda.get_device_name(0))

    # If not...
    else:
        print('No GPU available, using the CPU instead.')
        device = torch.device("cpu")


    testset = [['When is the birth date of <A> ?', 'When is the birthday of <A> ?'],
               ["When is the birth date of <A> ?", "When was <A> born ?"],
               ["When is the birth date of <A> ?", "Where does <A> come from ?"],
               ["When is the birth date of <A> ?","What is the birth name of <A> ?"],
               ["What is the ingredient of <A> ?","What is the Ingredient for <A> ?"],
               ["What is the ingredient of <A> ?","What is <A>'s ingredient ?"]]
    args = parser.parse_args()
    model = args.model
    # testset = args.testset
    model, tokenizer = load_model(model, device)
    pred_labels = predict(device, testset, model, tokenizer)
    for i, pair in enumerate(testset):
        print(" ".join(pair), pred_labels[i])