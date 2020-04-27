#!/usr/bin/env python
"""

Neural SPARQL Machines - Build the vocabulary.

'SPARQL as a Foreign Language' by Tommaso Soru and Edgard Marx et al., SEMANTiCS 2017
https://arxiv.org/abs/1708.07624

Version 1.0.0

Usage: python build_vocab.py data.en > vocab.en
"""
import numpy as np
from tensorflow.contrib import learn
import sys
import importlib
import io

importlib.reload(sys)

x_text = list()
with io.open(sys.argv[1], encoding="utf-8") as f:
    for line in f:
        x_text.append(str(line[:-1]))

vocabulary = set()

lang = sys.argv[1].split('.')[-1].lower()
# print lang

if lang == "sparql":

    for x in x_text:
        for t in x.split(" "):
            vocabulary.add(t)

else:  # any other language

    # x_text = ['This is a cat','This must be boy', 'This is a a dog']
    max_document_length = max([len(x.split(" ")) for x in x_text])

    # Create the vocabularyprocessor object, setting the max lengh of the documents.
    vocab_processor = learn.preprocessing.VocabularyProcessor(
        max_document_length)

    # Transform the documents using the vocabulary.
    x = np.array(list(vocab_processor.fit_transform(x_text)))

    # Extract word:id mapping from the object.
    vocab_dict = vocab_processor.vocabulary_._mapping

    # Sort the vocabulary dictionary on the basis of values(id).
    # Both statements perform same task.
    #sorted_vocab = sorted(vocab_dict.items(), key=operator.itemgetter(1))
    sorted_vocab = sorted(list(vocab_dict.items()), key=lambda x: x[1])

    # Treat the id's as index into list and create a list of words in the ascending order of id's
    # word with id i goes at index i of the list.
    vocabulary = set(list(zip(*sorted_vocab))[0])

    # split also by apostrophe

    to_remove = set()
    to_add = set()
    for t0 in vocabulary:
        if "'" in t0:
            to_remove.add(t0)
            for t1 in t0.split("'"):
                to_add.add(t1)
    for t0 in to_remove:
        vocabulary.remove(t0)
    for t0 in to_add:
        vocabulary.add(t0)

# print terms
for v in vocabulary:
    if v != "":
        print(v.encode("utf-8"))
