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

reload(sys)
sys.setdefaultencoding('utf-8') 

def name_temp(filename):
    sparql_file = open("name_en.sparql","w")
    en_file = open("name_en.en","w")
    name_number_label = open(" name_number_label.tsv",'w')
    name_number_uri = open("name_number_uri.tsv",'w')

    ret_list = jsonext.json_extractor(filename)
    print("\nIterating iver all json entities\n")
    label_uri = entity_uri_ext.entity_uri_ext(filename)
    label_list = label_uri.keys()

    for ret_val in tqdm(range(len(ret_list))):
        # Extracting entity name
        
        val =  ret_list[ret_val][2]
        regex = re.compile(r'\<[^\>]*\>') 
        mo = regex.findall(val)
        count = 0 
        name_uri = []
        name_label = []
        accum = []  
        accum_mo = []
        for mo_val in range(len(mo)):
            #ret_list[ret_val][1] = ret_list[ret_val][1].replace(label_uri[mo[mo_val][1:-1]],"name"+str(mo_val)+"") 
            regex_uri = re.compile(r'\<[^\>]*\>') 
            mo_uri = regex_uri.findall(ret_list[ret_val][1]) 

            flag = 1
            for mo_uri_val in mo_uri:
                last = mo_uri_val[1:-1].split("/")
                # print(last[-1].replace("_", " "),mo[1][1:-1] )
                percent =  SequenceMatcher(None, last[-1][1:-1].replace("_", " "),mo[mo_val][1:-1]).ratio()
                """ print [mo_uri_val,percent]
                print("****************") """
                if percent > 0.65:
                   
                    name_uri.append( mo_uri_val)
                    name_label.append(mo[mo_val])

                    ret_list[ret_val][1] = ret_list[ret_val][1].replace(mo_uri_val,"name_"+str(count)) 
                    ret_list[ret_val][2] = ret_list[ret_val][2].replace(mo[mo_val],"name_"+str(count)) 
                    
                    count+=1
                    
                    
                    accum.append(mo_uri_val[1:-1])
                    accum_mo.append(mo[mo_val] )
                    flag = 0
                    break
                    #print percent
                    #print(mo_val[1:-1]+ "\t\t\t\t\t" + mo_uri_val[1:-1])
            if(flag):
                synonyms = []
                for syn in wordnet.synsets(mo[mo_val][1:-1]):
                    for lm in syn.lemmas():
                            synonyms.append(lm.name())
                #print synonyms
                for words in mo[mo_val][1:-1].split(" "):
                    synonyms.append(words)
                for mo_uri_val in mo_uri:
                    last = mo_uri_val[1:-1].split("/")
                    # print(last[-1].replace("_", " "),mo[1][1:-1] )
                    for word in synonyms:
                        percent =  SequenceMatcher(None, last[-1][1:-1].replace("_", " "),word).ratio()
                        if percent > 0.65:
                            
                            
                            name_uri.append( mo_uri_val)
                            name_label.append(mo[mo_val])
                            ret_list[ret_val][1] = ret_list[ret_val][1].replace(mo_uri_val,"name_"+str(count)) 
                            ret_list[ret_val][2] = ret_list[ret_val][2].replace(mo[mo_val],"name_"+str(count)) 
                            count+=1
                            
                            accum.append(mo_uri_val[1:-1])
                            break
        if(len(accum)  < len (mo_uri)):
                space_string = ret_list[ret_val][2]
                for space_rem_val in accum_mo:
                    try:
                        space_string = space_string.replace(space_rem_val," ")
                    except:
                        print(space_rem_val)
                        return
                space_string =  space_string.replace(">","")
                space_string =  space_string.replace("<","")                
                stop = set(stopwords.words('english'))
                sentence = space_string
                lst = LancasterStemmer()
                space_list = ([lst.stem(i) for i in sentence.lower().split() if i not in stop])

                for mo_val in space_list:
                    """ print mo_val """
                    for mo_uri_val in mo_uri:
                        last = mo_uri_val[1:-1].split("/")
                        # print(last[-1].replace("_", " "),mo[1][1:-1] )
                        percent =  SequenceMatcher(None, last[-1][1:-1].replace("_", " "),mo_val).ratio()
                        """ print [mo_uri_val,percent]
                        print("****************") """
                        if percent > 0.60:
                            
                            
                            
                            name_uri.append( mo_uri_val)
                            name_label.append(mo_val)
                            ret_list[ret_val][1] = ret_list[ret_val][1].replace(mo_uri_val,"name_"+str(count))
                            ret_list[ret_val][2] = ret_list[ret_val][2].replace(mo_val,"name_"+str(count))
                            count+=1
                            
                            accum.append(mo_uri_val[1:-1])
                            accum_mo.append(mo_val )
                            break
 
        #print("*********")
        
        name_number_label.write(";".join(name_label)+"\n")
        name_number_uri.write(";".join(name_uri)+"\n")
        sparql_file.write(ret_list[ret_val][1]+"\n")
        en_file.write(ret_list[ret_val][2]+"\n")
        #print(1)
       
    print [len(ret_list)]       
    sparql_file.close()
    en_file.close()

    
   
    name_number_label.close()
    name_number_uri.close()

    list_liter = open("label_uri.tsv",'r').readlines()
    reread = open("name_en.sparql",'r').readlines()
    reread_en = open("name_en.en",'r').readlines()

    new_sparql = open("name_new.sparql",'w')
    new_en = open("name_new_en.en",'w')
    new_list_liter = open("name_new_label_uri.tsv",'w')

    for line in range(len(reread)):
        regex_uri = re.compile(r'\<[^\>]*\>') 
        mo_uri = regex_uri.findall(reread[line]) 
        for mo_uri_val in mo_uri:
            reread[line] = reread[line].replace(mo_uri_val,mo_uri_val.split("/")[-1][:-1].replace(" ","_"))
            list_liter.append(mo_uri_val.split("/")[-1] [:-1].replace(" ","_") + ";" + mo_uri_val+ "\n" )

        new_sparql.write(reread[line])
        
        regex_mo = re.compile(r'\<[^\>]*\>') 
        mo = regex_mo.findall(reread_en[line])
        for val_mo in mo:
            reread_en[line] = reread_en[line].replace(val_mo,val_mo[1:-1])
            
        new_en.write(reread_en[line])
    for list_val in list_liter:
        new_list_liter.write(list_val)

    dict_list_liter = {}
    for values in list_liter:
        values= values.split(";")
        dict_list_liter[values[0]] = values[1]
    import numpy as np
    print(len(dict_list_liter))
    return dict_list_liter


if __name__ == "__main__":
    name_temp(sys.argv[1])
