""" 
This code creates a test set making sure the following constraints are 
followed: 
- The vocabulary in the test set has been learned in a separate context in the 
train set.
- Frequency Thresholding: The vocabulary in the test set is present in the train 
set for a given number of times.
"""

from tqdm import tqdm
import json
import os

# Opening all the necessary fines and reading them.
train_vocab = open("vocab.sparql",'r').readlines()
test_sparql = open("old_test.sparql",'r').readlines()
train_sparql = open("train.sparql",'r').readlines()

accum = []

# List of all DBpedia resources in the vocabulary. 
dbr = []
for word in train_vocab:
    if(word.startswith('dbr')):
        dbr.append(word.strip())
print(len(dbr))

# List of all DBpedia ontologies in the vocabulary
dbo = []
for word in train_vocab:
    if(word.startswith('dbo')):
        dbo.append(word.strip())
print(len(dbo))
dbo_useful = []
dic = {}

print("Number of enteries in the test file SPARQL : "+ str(len(test_sparql)))

dbo_dic= {}
for temp in dbo:
        dbo_dic[temp] = 0

# Removing all the ontologies not present in the train vocabulary
for lines in tqdm(train_sparql):
    flag = 0
    for wor in lines.split(" "):
        for words in dbo:
                if(words == wor.strip()):
                        flag = 1
                        dbo_dic[wor] += 1
        """ if(wor.strip().startswith("dbo") and not flag):
                dbo_dic[wor] = 1
                dbo.append(wor) """
    if(flag):
        dbo_useful.append(lines)
        accum.append(lines)
accum = []
dbo_value = json.dumps(dbo_dic)

# Creating a dump of the frequency of the vacubulary counted.
open("dbo_dump_train.json",'w').write(dbo_value)

dbo_useful = []
dbo_dic= {}
for temp in dbo:
        dbo_dic[temp] = 0

# Removing all the ontologies not present in the train vocabulary
for lines in tqdm(test_sparql):
    flag = 0
    for wor in lines.split(" "):
        for words in dbo:
                if(words == wor.strip()):
                        flag = 1
                        dbo_dic[wor] += 1
                        continue
        if(wor.strip().startswith("dbo") and wor.strip() not in dbo):
                flag = 0
                break
        
        """ if(wor.strip().startswith("dbo") and not flag):
                dbo_dic[wor] = 1
                dbo.append(wor) """

    if(flag):
        dbo_useful.append(lines)
        accum.append(lines)

open("temp",'w').write("\n".join(dbo_useful))
dbo_value = json.dumps(dbo_dic)
# Creating a dump of the frequency of the vacubulary counted.
open("dbo_dump.json",'w').write(dbo_value)

print("After DBO:" +str(len(dbo_useful)))
accum = []


# Initializing the counter for resource vocabulary to 0
for temp in dbr:
        dic[temp] = 0

# Vocabulary frequency calculator
if(os.path.exists("dump.json")):
        dump = open("dump.json").read()
        load_dic = json.loads(dump)
        dic = load_dic
else:
        for lines in tqdm(train_sparql):
                for words in dbr:
                        for wor in lines.split(" "):
                                if(words == wor.strip()):
                                        dic[words]+=1
                                        break

print("Frequency Calculated")


# Removing all vocabulary with frequency less than a pre-defined threshold
dbr_refined = []
for key in dic.keys():
        if(dic[key] > 7):
                dbr_refined.append(key)
# Redifining dbr
dbr = dbr_refined
useful = []

print("Frequency thresholding completed")


# Removing all the entries in test with resource entity frequency
# Less than the pre-defined value.
for lines in tqdm(dbo_useful):
    flag = 1
    for words in dbr:
        for wor in lines.split(" "):
                if(words == wor.strip()):
                        flag = 0
                        useful.append(lines)
                        break
    if(flag):
        accum.append(lines)

print("After DBR:" +str(len(useful)))

open("stuff.sparql",'w').write(''.join(useful))


test_english = open("old_test.en",'r').readlines()
useful_en = []

# FInding the corresponding index and getting the matching natural
# Language questions.
for use in useful:
    index = test_sparql.index(use)
    useful_en.append(test_english[index])

open("stuff.en",'w').write(''.join(useful_en))

print (len(useful))
print(len(useful_en))

value = json.dumps(dic)
# Creating a dump of the frequency of the vacubulary counted.
open("dump.json",'w').write(value)