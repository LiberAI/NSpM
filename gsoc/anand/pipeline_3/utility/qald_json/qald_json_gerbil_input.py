from sklearn.metrics import f1_score
from interpreter import interpreter
import os
import numpy as np
from nltk.corpus import stopwords
import urllib
from bs4 import BeautifulSoup
from tqdm import tqdm
from collections import OrderedDict
import json

base = {"dataset":{"id": "stuff"}}
base["questions"] = []
question_lines = open('qald_json/test.en', 'r').readlines()
lines = open('qald_json/test.sparql', 'r').readlines()
lines = list(map(interpreter, tuple(lines)))

for valu in range(len(lines)):
        lines[valu] = lines[valu].replace("limit\n","limit 1\n")

#print("".join(lines))
#print(len(lines))

import urllib2
contents = urllib2.urlopen
accum = []
count = 0
stop = set(stopwords.words('english'))
for valu in tqdm(range(len(lines))):
        count+=1
        query = urllib.quote(lines[valu])
        url2 = "https://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query="+query+"&format=application%2Fsparql-results%2Bjson&CXML_redir_for_subjs=121&CXML_redir_for_hrefs=&timeout=30000&debug=on&run=+Run+Query+"
        #url2 = "https://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query="+query+"&format=text%2Fhtml&CXML_redir_for_subjs=121&CXML_redir_for_hrefs=&timeout=30000&debug=on&run=+Run+Query+"
        #page = urllib2.urlopen(url2)
        #soup = BeautifulSoup(page, "html.parser")
        try:
                page = urllib2.urlopen(url2)
        except:
                print(url2)
                continue
        soup = BeautifulSoup(page, "html.parser")
        js_dic = json.loads(str(soup))
        bindings = js_dic["results"]["bindings"]
        #print (bindings)
        answer = []
        #print("************")
        """ for rows in (soup.find_all("tr")):
                for td in rows.find_all("td"):
                        answer.append(td.getText())
        """
        que = {}
        que["id"] = str(valu)
        que["answertype"] = "resource" # Check
        que["aggregation"] = False
        que["onlydbo"] = True
        que["hybrid"] = False
        que["question"] = [{"language":"en", "string":question_lines[valu][:-1], "keywords" : " ".join([i for i in question_lines[valu].lower().split() if i not in stop] )}]
        que["query"] = {"sparql":lines[valu][:-1]}
        que["answers"] = []
        anc_accum = []
        #answer_unit = js_dic
        answer_unit =  {"head": {"vars": ["uri"]}}
        for ans in bindings: 
                ans = ans["x"]
                if("dbpedia" in ans):
                        temp = {"uri": {"type": ans["type"], "value": ans["value"]}}
                else:
                        temp = {"uri": {"type": ans["type"], "value": ans["value"]}} 
                anc_accum.append(temp)
        answer_unit["results"] = {}
        answer_unit["results"]["bindings"] = anc_accum
        que["answers"].append(answer_unit)
        accum.append(que)

        """ if(count>10):
                break """
        
base["questions"] = accum

import json
with open('qald_json/data.json', 'w') as outfile:
    json.dump(OrderedDict(base), outfile, ensure_ascii=False, indent=2)



