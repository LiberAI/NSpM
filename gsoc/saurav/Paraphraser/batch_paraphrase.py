import argparse
import os
import tensorflow as tf
import torch 
import gc
from tqdm import tqdm
tf.compat.v1.enable_eager_execution()
from paraphrase_questions import paraphrase_questions,prepare_model,set_seed,pick_final_sentence, pick_final_sentence_advanced
from constant import Constant
from bert_utils import write_data, load_model

seperator = ";"

def batch_paraphrase(templates_path, output_file, model_dir):

    set_seed(42)
    tokenizer, device, model = prepare_model()
    if model_dir:
        model_classifier, tokenizer_classifier = load_model(model_dir)
    dir = os.path.realpath(templates_path)
    final_data = []
    with open(dir, "r") as lines:
        for line in tqdm(lines):
            prop = line.strip("\n").split(seperator)
            question = prop[3]
            paraphrased_candidates = paraphrase_questions(tokenizer, device, model, question)
            paraphrased = pick_final_sentence(question, paraphrased_candidates)
            advanced = pick_final_sentence_advanced(device, question, paraphrased_candidates, model_classifier, tokenizer_classifier, paraphrased)
            final_data.append(line.strip('\n'))
            #print("Original", line)

            new_prop = prop[:-1]
            new_prop[3] = paraphrased
            new_prop.append("Paraphrased")
            new_line = seperator.join(new_prop)
            final_data.append(new_line)
            #print("Paraphrase", new_line)

            new_prop = prop[:-1]
            new_prop[3] = advanced
            new_prop.append("Paraphrased advanced")
            new_line = seperator.join(new_prop)
            final_data.append(new_line)
            #print("Advanced", new_line)

            # clean up memory
            torch.cuda.empty_cache()
            gc.collect()

    write_data(output_file, final_data)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--templates', dest='templates', metavar='templates file',
                               help='templates file', required=True)
    requiredNamed.add_argument('--output_file', dest='output_file', metavar='output file',
                               help='output file', required=True)
    requiredNamed.add_argument('--model', dest='model', metavar='model_dir',
                               help='path of directory of the fine-tuned model', required=True)


    args = parser.parse_args()
    templates_path = args.templates
    output_file = args.output_file
    model_dir = args.model
    batch_paraphrase(templates_path, output_file, model_dir)
