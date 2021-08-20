"""
Part of dbpedia/neural-qa 
Code for implementing Syntax Aware Data Augmentation on DBNQA 
"""


from gensim.models import Word2Vec
from nltk.corpus import stopwords
from nltk import word_tokenize
import networkx as nx
import numpy as np
import spacy
import math
import re

#import nltk
# nltk.download("stopwords")
# nltk.download("punkt")

nlp = spacy.load("en_core_web_sm")
regex = re.compile('[@_!#$%^&*()<>/\|}{~:]')
stoplist = stopwords.words('english')


def getData(textEn, textSP):
    pair = []
    pair.append(textEn)
    pair.append(textSP)
    return pair


def parsingTree(pair, alpha):
    doc = nlp(pair[0])
    edges = []
    nodes = []
    root_word = ""
    for w in doc:
        edges.append((w.head.text, w.text))
        nodes.append(w.text)
        if w.dep_ == "ROOT":
            root_word = w.text

    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)

    targetWords = []
    wordDepths = []

    for node in list(graph.nodes):
        try:
            d = nx.shortest_path_length(graph, source=root_word, target=node)
            targetWords.append(node)
            wordDepths.append(d)
        except nx.exception.NetworkXNoPath:
            pass

    prob = []

    for wD in wordDepths:
        if wD == 0:
            pass
        else:
            p = wD - 1
            d = math.pow(2, p)
            f = 1/d
            pr = 1 - f
            prob.append(pr)

    sigmoidin = []
    prob_ar = np.array(prob)
    for prob_a in prob_ar:
        sig = 1/(1+math.exp(-(prob_a)))
        sigmoidin.append(sig)
    sigmoid = np.array(sigmoidin)
    probFinal = sigmoid * alpha * float(len(sigmoidin))

    return probFinal


def top2(probs):
    arr = probs
    index1 = np.argmax(arr)
    arr[index1] = 0.0
    index2 = np.argmax(arr)

    return index1, index2


def dropout(en_sen, inde1, inde2):
    en_words = en_sen.split()
    sentence_len = len(en_words)
    if sentence_len >= 12:
        en_words[inde1] = ""
        en_words[inde2] = ""
    else:
        en_words[inde1] = ""
    final = " ".join(en_words)

    return final


def get_syn_lex(path):
    syn_lexicon = {}
    text = [l.strip("?") for l in open(path).readlines()]
    for t in text:
        t = t.split()
        k = t[0]
        v = t[1:len(t)]
        syn_lexicon[k] = v
    return syn_lexicon


def replacement(en_sen, inde1, inde2):
    synonyms_lexicon = get_syn_lex('gsoc/siddhant/DataAug/Syntax-aware/syn.txt')
    keys = synonyms_lexicon.keys()
    en_sen = en_sen.strip('?')
    words = word_tokenize(en_sen)
    sen = en_sen
    en_words = en_sen.split()

    for w in words:
        if w not in stoplist:
            if w in keys:
                sen = sen.replace(w, synonyms_lexicon[w][0])

    return sen + " ?"


""" def wordvec_replacement(en_sen, inde1, inde2):
    model = Word2Vec.load(
        "gsoc/siddhant/DataAug/vec.pkl")
    en_sen = en_sen.strip('?')
    en_words = en_sen.split()
    sentence_len = len(en_words)
    if sentence_len >= 12:
        if not(en_words[inde1].isdigit() or en_words[inde2].isdigit() or regex.search(en_words[inde1]) == None or regex.search(en_words[inde2]) == None):
            word1 = model.wv[en_words[inde1]].lower()
            word2 = model.wv[en_words[inde2]].lower()
            replace1 = model.wv.most_similar([word1], topn=2)[1][0]
            replace2 = model.wv.most_similar([word2], topn=2)[1][0]
            en_words[inde1] = replace1
            en_words[inde2] = replace2
        else:
            exit
    else:
        if not(en_words[inde1].isdigit() or regex.search(en_words[inde1]) == None):
            word1 = model.wv[en_words[inde1]]
            replace1 = model.wv.most_similar([word1], topn=2)[1][0]
            en_words[inde1] = replace1
        else:
            exit
    final = " ".join(en_words)
    final = final + " ?"
    return final
 """


def blanking():
    pass


if "__name__" == "__main__":
    pass