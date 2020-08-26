import argparse
import tensorflow as tf
tf.compat.v1.enable_eager_execution()
from paraphrase_questions import paraphrase_questions,get_pretrained_model,prepare_model,set_seed,pick_final_sentence, pick_final_sentence_advanced
from constant import Constant

const = Constant()
seperator = "\t"

const.URL = "https://datascience-models-ramsri.s3.amazonaws.com/t5_paraphraser.zip"

def batch_paraphrase(templates_path, model_dir):
    folder_path = get_pretrained_model(const.URL)
    set_seed(42)
    tokenizer, device, model = prepare_model(folder_path)
    with open(templates_path, "r") as lines:
        with open(templates_path + "_paraphrased", "w") as w:
            for line in lines:
                prop = line.strip("\n").split(seperator)
                question = prop[3]
                paraphrased_candidates = paraphrase_questions(tokenizer, device, model, question)
                paraphrased = pick_final_sentence(question, paraphrased_candidates)
                advanced = pick_final_sentence_advanced(device, question, paraphrased_candidates, model_dir)
                w.write(line)
                # for i, candidate in enumerate(paraphrased_candidates):
                #     new_prop = prop[:-1]
                #     new_prop[3] = candidate
                #     new_prop.append("Paraphrased {}\n".format(i))
                #     print(new_prop)
                #     new_line = seperator.join(new_prop)
                #
                #     w.write(new_line)
                new_prop = prop[:-1]
                new_prop[3] = paraphrased
                new_prop.append("Paraphrased \n")
                new_line = seperator.join(new_prop)
                w.write(new_line)
                new_prop = prop[:-1]
                new_prop[3] = advanced
                new_prop.append("Paraphrased advanced\n")
                new_line = seperator.join(new_prop)
                w.write(new_line)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--templates', dest='templates', metavar='templates file',
                               help='templates file', required=True)
    requiredNamed.add_argument('--model', dest='model', metavar='model_dir',
                               help='path of directory of the fine-tuned model', required=True)


    args = parser.parse_args()
    templates_path = args.templates
    model_dir = args.model
    batch_paraphrase(templates_path, model_dir)
