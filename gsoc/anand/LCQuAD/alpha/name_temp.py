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
 

""" def name_temp2(filename):
    sparql_file = open("en.sparql","w")
    en_file = open("en.en","w")
    ret_list = jsonext.json_extractor(filename)
    print("\nIterating iver all json entities\n")
    label_uri = entity_uri_ext.entity_uri_ext()
    label_list = label_uri.keys()
    for ret_val in tqdm(range(len(ret_list))):
        # Extracting entity name
        val =  ret_list[ret_val][2]
        regex = re.compile(r'\<[^\>]*\>') 
        mo = regex.findall(val)
        count = 0 
        for mo_val in range(len(mo)):
            
            ret_list[ret_val][2] = ret_list[ret_val][2].replace(mo[mo_val],"<name"+str(mo_val)+">") 
            
            #ret_list[ret_val][1] = ret_list[ret_val][1].replace(label_uri[mo[mo_val][1:-1]],"name"+str(mo_val)+"") 
            regex_uri = re.compile(r'\<[^\>]*\>') 
            mo_uri = regex_uri.findall(ret_list[ret_val][1]) 

            for mo_uri_val in mo_uri:
                last = mo_uri_val[1:-1].split("/")
                # print(last[-1].replace("_", " "),mo[1][1:-1] )
                percent =  SequenceMatcher(None, last[-1][1:-1].replace("_", " "),mo[mo_val][1:-1]).ratio()
                if percent > 0.75:
                    ret_list[ret_val][1] = ret_list[ret_val][1].replace(mo_uri_val,"<name"+str(mo_val)+">") 
                    #print percent
                    #print(mo_val[1:-1]+ "\t\t\t\t\t" + mo_uri_val[1:-1])
        try:
            en_file.write(ret_list[ret_val][2]+"\n")
            sparql_file.write(ret_list[ret_val][1]+"\n")
        except:
            pass
            
    sparql_file.close()
    en_file.close()
    return ret_list
 """
def name_temp(filename):
    sparql_file = open("en.sparql","w")
    en_file = open("en.en","w")
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
        accum = []  
        accum_mo = []
        for mo_val in range(len(mo)):
            
            ret_list[ret_val][2] = ret_list[ret_val][2].replace(mo[mo_val],"$"+mo[mo_val][1:-1].replace(" ","_")+"$") 
            
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
                    
                    if __name__ == "__main__":
                        try:
                            ret_list[ret_val][1] = ret_list[ret_val][1].replace(mo_uri_val,"$"+mo[mo_val][1:-1].replace(" ","_")+"$") 
                            
                        except:
                            pass
                    
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
                            if __name__ == "__main__":
                                try:
                                    ret_list[ret_val][1] = ret_list[ret_val][1].replace(mo_uri_val,"$"+mo[mo_val][1:-1]+"$") 
                                    
                                except:
                                    pass
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
                            
                            if __name__ == "__main__":
                                try:
                                    ret_list[ret_val][1] = ret_list[ret_val][1].replace(mo_uri_val,"$"+mo_val.replace(" ","_")+"$")
                                    
                                except:
                                    pass
                            accum.append(mo_uri_val[1:-1])
                            accum_mo.append(mo_val )
                            break 

        """ for mo_uri_val in mo_uri:
            last = mo_uri_val[1:-1].split("/")
            # print(last[-1].replace("_", " "),mo[1][1:-1] )
            percent =  SequenceMatcher(None, last[-1][1:-1].replace("_", " "),mo[mo_val][1:-1]).ratio()
            if percent > 0.75:
                ret_list[ret_val][1] = ret_list[ret_val][1].replace(mo_uri_val,"<name"+str(mo_val)+">") 
                #print percent
                #print(mo_val[1:-1]+ "\t\t\t\t\t" + mo_uri_val[1:-1]) """
        try:
            
            sparql_file.write(ret_list[ret_val][1]+"\n")
            en_file.write(ret_list[ret_val][2]+"\n")
        except:
            pass
            
    sparql_file.close()
    en_file.close()

    list_liter = open("label_uri.tsv",'r').readlines()
    reread = open("en.sparql",'r').readlines()
    new_sparql = open("new.sparql",'w')
    new_list_liter = open("new_label_uri.tsv",'w')
    for line in range(len(reread)):
        regex_uri = re.compile(r'\<[^\>]*\>') 
        mo_uri = regex_uri.findall(reread[line]) 
        for mo_uri_val in mo_uri:
            reread[line] = reread[line].replace(mo_uri_val,"$"+mo_uri_val.split("/")[-1][:-1].replace(" ","_")+"$")
            list_liter.append(mo_uri_val.split("/")[-1] [:-1].replace(" ","_") + ";" + mo_uri_val+ "\n" )

        new_sparql.write(reread[line])
    for list_val in list_liter:
        new_list_liter.write(list_val)

    return ret_list


if __name__ == "__main__":
    name_temp(sys.argv[1])
