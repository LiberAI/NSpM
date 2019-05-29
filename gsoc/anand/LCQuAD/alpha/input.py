import jsonext
import re 
from difflib import SequenceMatcher
from tqdm import tqdm
import entity_uri_ext
import sys
from nltk.stem.lancaster import LancasterStemmer
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import name_tag_templates
import numpy as np

reload(sys)
sys.setdefaultencoding('utf-8') 

def tailoring(sentence,dict_list_vocab,dict_list_keys,temp_file,count):
    rev_range = range(len(sentence.split(" ")))
    rev_range.reverse()
    entity_dic = {}
    sen_list = sentence.split(" ")
    stop = set(stopwords.words('english'))
    for val in rev_range:
        accum = []
        for i in range(len(sen_list)):
            if(i+val+1<=len(sen_list)):
                accum.append(sen_list[i:i+val+1])
        for accum_val in accum:
            temp = "_".join(accum_val)
            
            if temp in stop:
                continue
            for dict_key in dict_list_keys:
                percent =  SequenceMatcher(None, dict_key,temp.replace("_"," ")).ratio()
                if percent > 0.85:
                    count+=1
                    print(sentence.replace(temp.replace("_"," "),"<name_"+str(count)+">"))
                    temp_file.write(sentence.replace(temp.replace("_"," "),"<name_"+str(count)+">")+","+dict_key+","+dict_list_vocab[dict_key][:-1]+","+"<name_"+str(count)+">\n")
                    tailoring(sentence.replace(temp.replace("_"," "),"<name_"+str(count)+">"),dict_list_vocab,dict_list_keys,temp_file,count)
                    return
                if percent > 0.80:
                    #print [dict_key,temp.replace("_"," "),percent]
                    try:
                        if entity_dic[dict_key][1] < percent:
                            entity_dic[dict_key]  = [temp.replace("_"," "),percent]
                            continue
                    except:
                        pass
                    entity_dic[dict_key]  = [temp.replace("_"," "),percent]
    print entity_dic               

def preprocess(filename,sentence):
    name_number_label = open(" input_label.tsv",'w')
    name_number_uri = open("input_uri.tsv",'w')
    processed_sentence =  open("proc_sen.tsv",'w')
    dict_list_vocab = name_tag_templates.name_temp(filename)
    dict_list_keys = dict_list_vocab.keys()
    count = -1
    temp_file = open("test.csv",'w')
    tailoring(sentence,dict_list_vocab,dict_list_keys,temp_file,count)
    return
    rev_range = range(len(sentence.split(" ")))
    rev_range.reverse()
    entity_dic = {}
    sen_list = sentence.split(" ")
    for val in rev_range:
        accum = []
        for i in range(len(sen_list)):
            if(i+val+1<=len(sen_list)):
                accum.append(sen_list[i:i+val+1])
        for accum_val in accum:
            temp = "_".join(accum_val)
            for dict_key in dict_list_keys:
                percent =  SequenceMatcher(None, dict_key,temp.replace("_"," ")).ratio()
                if percent > 0.80:
                    #print [dict_key,temp.replace("_"," "),percent]
                    try:
                        if entity_dic[dict_key][1] < percent:
                            entity_dic[dict_key]  = [temp.replace("_"," "),percent]
                            continue
                    except:
                        pass
                    entity_dic[dict_key]  = [temp.replace("_"," "),percent]
    print entity_dic               

    return
    space_string = sentence            
    stop = set(stopwords.words('english'))
    sentence = space_string
    lst = LancasterStemmer()
    space_list = ([(i) for i in sentence.lower().split() if i not in stop])
    print space_list
    count = 0
    name_label = []
    name_uri = []
    for mo_val in space_list:
        flag = 1
        for dict_key in dict_list_keys:
            """ print mo_val
            print dict_key """
            percent =  SequenceMatcher(None, dict_key.replace("_", " "),mo_val).ratio()
            if percent > 0.70 :
                name_uri.append(dict_list_vocab[dict_key][:-1])
                name_label.append(dict_key)
                sentence= sentence.replace(mo_val,"name_"+str(count))
                count+=1
                flag = 0
                break
        if(flag):
            flag2 = 1
            synonyms = []
            for syn in wordnet.synsets(mo_val):
                for lm in syn.lemmas():
                        synonyms.append(lm.name())
            #print synonyms
            for words in mo_val.split(" "):
                synonyms.append(words)
            stem_list = lst.stem(mo_val)
            synonyms.append(stem_list)

            for syno in synonyms:
                if(flag2==0):
                    break
                for dict_key in dict_list_keys:
                    percent =  SequenceMatcher(None, dict_key.replace("_", " "),syno).ratio()
                    if percent > 0.70:
                        name_uri.append(dict_list_vocab[dict_key][:-1])
                        name_label.append(mo_val)
                        sentence= sentence.replace(mo_val,"name_"+str(count))
                        count+=1
                        flag2 = 0
                        break
    processed_sentence.write(sentence)
    name_number_label.write(";".join(name_label))
    name_number_uri.write(";".join(name_uri))
    return

if __name__ == "__main__":
    preprocess(sys.argv[1], sys.argv[2])
