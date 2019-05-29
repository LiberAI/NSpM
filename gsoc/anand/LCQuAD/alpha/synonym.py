from nltk.corpus import wordnet
import nltk 
nltk.download('wordnet')
synonyms = []

for syn in wordnet.synsets("people"):
    for lm in syn.lemmas():
             synonyms.append(lm.name())
print (set(synonyms))