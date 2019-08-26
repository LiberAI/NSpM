"""
This code extracts all the embeddings from the pageRank.txt and records the following information in the following manner.

<name of embedding>\t<line number>\t<File number> 

This index will contain information regarding the position of all the words so that the corresponding embeddings can be extracted easily. Withput having to query through the whole embedding file.
"""

import sys
import os
from tqdm import tqdm 

a = [f for f in os.listdir("data_fragments/")]
for files in tqdm(a):
    #print(files)
    lines = open("data_fragments/"+files).readlines()
    writer = open("index.csv",'a')
    for line in range(len(lines)):
        lines[line] = lines[line].split("\t")
        word = lines[line][0]
        if "http://dbpedia.org/resource/" in (word):
            word = word.replace("http://dbpedia.org/resource/","dbr_")
        if "http://dbpedia.org/ontology/" in (word):
            word = word.replace("http://dbpedia.org/ontology/","dbo_")
        writer.write('\t'.join([word,files,str(line)])+'\n')
    writer.close()