import random
from collections import Counter

def return_data(file):
    texts = []
    with open(file, "rt") as myfile:
        for myline in myfile:
            myline = myline.strip()
            texts.append(myline)

    return texts


def randomset(text_en, text_sp, setsize):
    shuffle_en = []
    shuffle_sp = []
    index = random.sample(range(1, len(text_en)), setsize)
    for ind in index:
        shuffle_en.append(text_en[ind])
        shuffle_sp.append(text_sp[ind])

    return shuffle_en, shuffle_sp


def unigram_freq(val, n):
	return [val[i:i+n] for i in range(len(val)-n+1)]

def splits(text, n):
    text = text.strip('?')
    tokens = text.split()
    return [' '.join(val) for val in unigram_freq(tokens, n)]

def unicounter(corpus, n):
    return Counter(ngram for text in corpus for ngram in splits(text, n))

