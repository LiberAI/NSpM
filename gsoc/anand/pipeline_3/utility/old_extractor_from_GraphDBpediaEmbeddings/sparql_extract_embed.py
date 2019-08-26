from tqdm import tqdm
reader = open("pageRank.txt",'r')
vocab = open("vocab.sparql",'r').readlines()
count = 0
temp = ""
dict_vocab = []
vocab_count = 0
expected_count= 5774165
for val in tqdm(range(expected_count)):
    line = reader.readline()
    if(line == temp):
        break
    count+=1
    temp = line

    #print(line)
    line = line.split("\t")
    if "http://dbpedia.org/resource/" in (line[0]):
        line[0] = line[0].replace("http://dbpedia.org/resource/","dbr_")
    if "http://dbpedia.org/ontology/" in (line[0]):
        line[0] = line[0].replace("http://dbpedia.org/ontology/","dbo_")
    for words in vocab:
        if(words.strip() == line[0]):
            vocab_count+=1
            dict_vocab.append(words.strip() +" " +" ".join(line[1:]))
            #print(words.strip())
            break
print(count)
print(vocab_count)
reader.close()

writer = open("new_vocab.sparql",'w').write("\n".join(dict_vocab))
