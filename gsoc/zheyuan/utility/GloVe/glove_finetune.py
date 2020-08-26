import argparse
import csv
import numpy as np
from collections import Counter
from nltk.corpus import brown
from mittens import GloVe, Mittens
from sklearn.feature_extraction import stop_words
from sklearn.feature_extraction.text import CountVectorizer


def glove2dict(glove_filename):
    with open(glove_filename, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=' ', quoting=csv.QUOTE_NONE)
        embed = {line[0]: np.array(list(map(float, line[1:])))
                for line in reader}
    return embed

def batch_finetune(finetune_glove, batch_word):
    oov = [token for token in batch_word if token not in finetune_glove.keys()]

    en_doc = [' '.join(batch_word)]

    corp_vocab = list(set(oov))
    cv = CountVectorizer(ngram_range=(1,1), vocabulary=corp_vocab)
    X = cv.fit_transform(en_doc)
    Xc = (X.T * X)
    Xc.setdiag(0)
    coocc_ar = Xc.toarray()

    mittens_model = Mittens(n=300, max_iter=1800)
    new_embeddings = mittens_model.fit(
      coocc_ar,
      vocab=corp_vocab,
      initial_embedding_dict=finetune_glove)

    newglove = dict(zip(corp_vocab, new_embeddings))
    finetune_glove.update(newglove)
    return finetune_glove

def calculate_unknown(finetune_glove):
    vecs = np.zeros((len(finetune_glove), 300), dtype=np.float32)
    for i, key in enumerate(finetune_glove):
        vecs[i] = np.array(finetune_glove[key], dtype=np.float32)
    unknown = np.mean(vecs, axis=0)
    return unknown

def finetune_glove(project_path, glove_path="glove.6B.300d.txt"):
    word_en = []
    with open(project_path+"/data.en", "r") as lines:
        for sentence in lines:
            sentence = sentence.strip("\n")
            sentence = "<s> " + sentence + " </s>"
            for word in sentence.split():
                word_en.append(word.strip(":").strip("\"").strip("»").strip("+").strip("?").replace("i̇", ""))
    print(len(word_en), word_en[:20])

    vocab_en = list(set(word_en) - set(["<s>", "</s>"]))

    pre_glove = glove2dict(glove_path)
    stride = 700000
    start = 0
    end = start+stride
    finetune_glove = pre_glove.copy()
    while end<len(word_en):
        print("Start: ", start, "End: ", end)
        word_split = word_en[start:end]
        finetune_glove = batch_finetune(finetune_glove, word_split)
        start = end
        end = start + stride
    finetune_glove = batch_finetune(finetune_glove, word_en[start:])
    unk = calculate_unknown(finetune_glove)
    finetune_glove["<UNK>"] = unk
    with open(project_path+"/embed.en", "w") as w:
        for word in finetune_glove:
            w.write(word + " " + str(list(finetune_glove[word])).replace("[", "").replace("]", "").replace(",", "") + "\n")

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--path', dest='path', metavar='path',
                               help='path of project that contains the data..eb/sparql files', required=True)
    args = parser.parse_args()
    path = args.path
    finetune_glove(path, "glove.6B/glove.6B.300d.txt")
    pass