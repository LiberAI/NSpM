import argparse
from bert_utils import read, write_data

def process_data(data):

    original = ""
    final_data = []
    for sub_data in data:
        paraphrase = ""
        split = sub_data.split(';')
        type = split[-1].strip()
        print(type)
        if type == 'Original':
            original = sub_data
        else:
            if len(type.split()) == 1: # Annotated data - -1, 0, 1
                paraphrase = sub_data
        
        if original != "" and paraphrase != "":
            final_data.append(original.split(';')[3]+";"+paraphrase.split(';')[3]+";"+paraphrase.split(';')[-1])

    return final_data

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--templates', dest='templates', metavar='templates file',
                               help='templates file', required=True)

    args = parser.parse_args()
    templates_path = args.templates
    data = read(templates_path)
    final_data = process_data(data)
    write_data('gsoc/saurav/Paraphraser/Data/train.txt', final_data)