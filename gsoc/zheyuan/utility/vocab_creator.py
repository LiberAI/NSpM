import argparse
from tqdm import tqdm

def english_vocab(project_path):
    print("Creating english vocabulary")
    vocab_en = []
    word_en = []
    with open(project_path+"/data.en", "r") as lines:
        for sentence in tqdm(lines):
            sentence = sentence.strip("\n")
            for word in sentence.split():
                word_en.append(word.strip(":").strip("\"").strip("»").strip("+").strip("?"))

    vocab_en = list(set(word_en))
    vocab_en.remove("")
    with open(project_path+"/vocab.en", "w") as w:
        for vocab in vocab_en:

            w.write(vocab.strip() + "\n")

def sparql_vocab(project_path):
    print("Creating SPARQL vocabulary")

    vocab_sparql = []
    with open(project_path+"/data.sparql", "r") as lines:
        for sentence in tqdm(lines):
            sentence = sentence.strip("\n")
            for word in sentence.split():
                if word == "dbr_Flying_Legend":
                    print(sentence)
                vocab_sparql.append(word)
    vocab_sparql = list(set(vocab_sparql))
    with open(project_path+"/vocab.sparql", "w") as w:
        for vocab in vocab_sparql:
            w.write(vocab.strip() + "\n")

def add_s_tokens(path):
    with open(path+"/data.sparql", "r") as lines:
        with open("./GloVe/GloVe-master/data_s.sparql", "w") as w:
            for line in lines:
                new_line = "<s> " + line.strip() + " </s>\n"
                w.write(new_line)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--path', dest='path', metavar='path',
                               help='path of project that contains the data.en/sparql files', required=True)
    args = parser.parse_args()
    path = args.path
    english_vocab(path)
    sparql_vocab(path)
    add_s_tokens(path)
    pass