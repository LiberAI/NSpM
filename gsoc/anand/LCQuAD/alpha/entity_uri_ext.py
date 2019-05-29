import jsonext
import re 
import sys
from difflib import SequenceMatcher
from tqdm import tqdm
from nltk.stem.lancaster import LancasterStemmer
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
 

def entity_uri_ext(filename):
    ct = 0
    label_uri_ret_val = {}
    if __name__ == "__main__":
        label_uri = open("label_uri.tsv",'w')
    ret_list = jsonext.json_extractor(filename)
    print("\nInteration over all the enteries to extract URI label pair\n")
    for ret_val in tqdm(ret_list):
        # Extracting entity name
        val =  ret_val[2]
        regex = re.compile(r'\<[^\>]*\>') 
        mo = regex.findall(val) 

        # Extracting entity name 
        val_uri =  ret_val[1]
        regex_uri = re.compile(r'\<[^\>]*\>') 
        mo_uri = regex_uri.findall(val_uri) 
        # Finding the match based on matching probability 
        accum = []  
        accum_mo = []

        for mo_val in mo:
            flag = 1
            for mo_uri_val in mo_uri:
                last = mo_uri_val[1:-1].split("/")
                # print(last[-1].replace("_", " "),mo[1][1:-1] )
                percent =  SequenceMatcher(None, last[-1][1:-1].replace("_", " "),mo_val[1:-1]).ratio()
                """ print [mo_uri_val,percent]
                print("****************") """
                if percent > 0.70:
                    
                    if __name__ == "__main__":
                        try:
                            label_uri.write( mo_val[1:-1] +";"+ mo_uri_val[1:-1] +"\n")
                        except:
                            pass
                    label_uri_ret_val[mo_val[1:-1]] =  mo_uri_val[1:-1]
                    accum.append(mo_uri_val[1:-1])
                    accum_mo.append(mo_val )
                    flag = 0
                    #print percent
                    #print(mo_val[1:-1]+ "\t\t\t\t\t" + mo_uri_val[1:-1])
            if(flag):
                synonyms = []
                for syn in wordnet.synsets(mo_val[1:-1]):
                    for lm in syn.lemmas():
                            synonyms.append(lm.name())
                #print synonyms
                for words in mo_val[1:-1].split(" "):
                    synonyms.append(words)
                for mo_uri_val in mo_uri:
                    last = mo_uri_val[1:-1].split("/")
                    # print(last[-1].replace("_", " "),mo[1][1:-1] )
                    for word in synonyms:
                        percent =  SequenceMatcher(None, last[-1][1:-1].replace("_", " "),word).ratio()
                        if percent > 0.70:
                            if __name__ == "__main__":
                                try:
                                    #print "hi"
                                    label_uri.write( mo_val[1:-1] +";"+ mo_uri_val[1:-1] +"\n")
                                    label_uri.write( word +";"+ mo_uri_val[1:-1] +"\n")    
                                except:
                                    pass
                            label_uri_ret_val[mo_val[1:-1]] =  mo_uri_val[1:-1]
                            label_uri_ret_val[word] =  mo_uri_val[1:-1]
                            accum.append(mo_uri_val[1:-1])
                #print mo_val[1:-1]
                #return
        if(len(accum)  < len (mo_uri)):
                space_string = ret_val[2]
                for space_rem_val in accum_mo:
                    space_string = space_string.replace(space_rem_val," ")
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
                        if percent > 0.70:
                            
                            if __name__ == "__main__":
                                try:
                                    label_uri.write( mo_val +";"+ mo_uri_val[1:-1] +"\n")
                                except:
                                    pass
                            label_uri_ret_val[mo_val] =  mo_uri_val[1:-1]
                            accum.append(mo_uri_val[1:-1])
                            accum_mo.append(mo_val )
                            #print percent
                            #print(mo_val[1:-1]+ "\t\t\t\t\t" + mo_uri_val[1:-1])
                """ print("\n") 
                print"------------"
                print len(accum)
                print accum
                return """

    if __name__ == "__main__":        
        label_uri.close()
    return label_uri_ret_val

if __name__ == "__main__":
    entity_uri_ext(sys.argv[1])
