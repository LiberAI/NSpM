import json
from tqdm import tqdm
import os 
index = open("index.csv").readlines()
diction = {}
missed_counter = 0
print("""
Loading the index information from the index.csv file.
""")

for line in tqdm(range(len(index))):
    index[line] = index[line].split('\t')
    key = index[line][0].strip()
    diction[key] = {}
    diction[key]['file'] = index[line][1]
    diction[key]['line'] = index[line][2].strip()
""" 
This part of the code creates the a json file containing the information which can be loaded easily.
"""
""" 
with open("data_file.json", "w") as write_file:
    json.dump(diction, write_file) 
"""

file_diction = {}

a = [f for f in os.listdir("data_fragments")]

for val in (a):
    file_diction[val.strip()] = []

vocab = open("vocab.sparql",'r').readlines()
filename = []
dict_keys = diction.keys()

print("""
Checking and accumulating information for words obtained from the vocabulary from the index thus loaded. 
""")

for word in tqdm(vocab):
    word = word.strip()
    if(word in dict_keys ):
        file_diction[diction[word]["file"]].append(diction[word])
    else:
        missed_counter+=1


print(""" 
Loading information from the broken files to extract the required embeddings.
""")
accum = []
for files in tqdm(a): 
    file_reader = open("data_fragments/"+files).readlines()
    for words_in_file in file_diction[files.strip()]:
        accum.append(file_reader[int(words_in_file["line"].strip())].strip()) 

print(""" 
Writing the extracted embeddings in a file for future use. 
""")
final = ("\n".join(accum)).replace('\t',' ')
final = final.replace("http://dbpedia.org/resource/","dbr_")
final = final.replace("http://dbpedia.org/ontology/","dbo_")
open("new_vocbulary.csv",'w').write(final)

print("Missed words: "+str(missed_counter))



        



