import tensorflow_hub as hub
import tensorflow as tf
import zipfile
import requests, zipfile, io
import os
import re
import argparse
import torch
from transformers import T5ForConditionalGeneration,T5Tokenizer
# pip install transformers==2.9.0
from constant import Constant
from textual_similarity import similarity

const = Constant()

const.URL = "https://datascience-models-ramsri.s3.amazonaws.com/t5_paraphraser.zip"

def get_pretrained_model(zip_file_url):
    """

    @param zip_file_url: This url references to the download link of the pre-trained model
    @return: folder_path: path to store the pre-trained model
    """
    model_name = zip_file_url.split("/")[-1].replace(".zip", "")
    folder_path = './{}'.format(model_name)
    print('Get pretained model {}'.format(model_name))

    if not os.path.exists(folder_path):
        r = requests.get(zip_file_url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(folder_path)
    else:
        print("Folder available: ", folder_path)

    print('Finish {}'.format(model_name))
    return folder_path

def prepare_model(folder_path):
    """

    @param folder_path: This path contains the pre-trained model
    @return: Tokenizer, Device, Model
    """
    model = T5ForConditionalGeneration.from_pretrained(folder_path)
    tokenizer = T5Tokenizer.from_pretrained('t5-base')

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("device ", device)
    model = model.to(device)
    return tokenizer, device, model

def set_seed(seed):
  torch.manual_seed(seed)
  if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)


def paraphrase_questions(tokenizer, device, model, sentence):
    """

    @param tokenizer: Tokenizer is in charge of preparing the inputs for a model
    @param device: Device the model will be run on
    @param model: The pre-trained model
    @param sentence: The sentence need to be paraphrased
    @return: final_outputs: a num_return_sequences*2 matrix, each row contains an array [paraphrased_sentence, semantic_similarity]
    """
    sentence = sentence.replace("<A>", "XYZ")

    text = "paraphrase: " + sentence + " </s>"

    max_len = 256

    encoding = tokenizer.encode_plus(text, pad_to_max_length=True, return_tensors="pt")
    input_ids, attention_masks = encoding["input_ids"].to(device), encoding["attention_mask"].to(device)
    beam_outputs = model.generate(
        input_ids=input_ids, attention_mask=attention_masks,
        do_sample=True,
        max_length=256,
        top_k=120,
        top_p=0.98,
        early_stopping=True,
        num_return_sequences=10
    )
    print("\nOriginal Question ::")
    print(sentence)
    print("\n")
    print("Paraphrased Questions :: ")
    final_outputs = []
    for beam_output in beam_outputs:
        sent = tokenizer.decode(beam_output, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        if sent.lower() != sentence.lower() and sent not in final_outputs:
            sent = re.sub('XYZ', '<A>', sent, flags=re.IGNORECASE)
            final_outputs.append([sent])

    for i, final_output in enumerate(final_outputs):
        print("{}: {}".format(i, final_output[0]))
        semantic_similarity = similarity(sentence, final_output[0])
        final_output.append(semantic_similarity)
    return final_outputs





if __name__ == "__main__":
    """
    Section for testing the function of the Paraphraser
    """
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--sentence', dest='sentence', metavar='sentence',
                                                            help='sentence', required=True)

    args = parser.parse_args()
    sentence = args.sentence


    folder_path = get_pretrained_model(const.URL)
    set_seed(42)
    tokenizer, device, model = prepare_model(folder_path)
    print(paraphrase_questions(tokenizer,device,model,sentence))
    pass