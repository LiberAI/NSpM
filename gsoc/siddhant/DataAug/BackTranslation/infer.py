import random
from numpy import argmax
import numpy as np
from nltk.translate.bleu_score import sentence_bleu

def clean(str):
  punc = '!"#$%&()*+,-./:;<=>?@[\\]^\'`{|}~'
  for s in str:
    if s in punc:
      str = str.replace(s, "")
  return str

# map an integer to a word
def word_for_id(integer, tokenizer):
	for word, index in tokenizer.word_index.items():
		if index == integer:
			return word
	return None
 
# generate target given source sequence
def predict_sequence(model, tokenizer, source):
	prediction = model.predict(source, verbose=0)[0]
	integers = [argmax(vector) for vector in prediction]
	target = list()
	for i in integers:
		word = word_for_id(i, tokenizer)
		if word is None:
			break
		target.append(word)
	return ' '.join(target)


# evaluate the skill of the model
def translate_batch(model, tokenizer, sources, target):
    actual, predicted = list(), list()
    for i, source in enumerate(sources):
		# translate encoded source text
        source = source.reshape((1, source.shape[0]))
        translation = predict_sequence(model, tokenizer, source)
		

        actual.append([target])
        predicted.append(translation)
        
    return (target, predicted)


def predict_sequence_tokenized(model, source):
    prediction = model.predict(source, verbose=0)[0]
    integers = [argmax(vector) for vector in prediction]
    return integers

def randomset(text_en, text_sp, setsize):
    shuffle_en = []
    shuffle_sp = []
    index = random.sample(range(1, len(text_en)), setsize)
    for ind in index:
        shuffle_en.append(text_en[ind])
        shuffle_sp.append(text_sp[ind])

    return shuffle_en, shuffle_sp


def bleuscore(model, eng_tokenizer, testX, en_sub_test):
    a = testX
    b = en_sub_test
    batch_size = 64
    scores = []
    for i in range(int(len(a)/batch_size)):
        score = 0
        target, predicted = translate_batch(model, eng_tokenizer, a[(batch_size*i):(batch_size*(i+1))], b[(batch_size*i):(batch_size*(i+1))])
        for j in range(len(predicted)):
            score += sentence_bleu([clean(target[j]).split()], predicted[j].split(), weights=(0.25, 0.25, 0.25, 0.25))
        
        score = score/len(predicted)
        scores.append(score)
    
    scores = np.array(scores)
    bleu = np.mean(scores)
    print('bleu score for given model {}'.format(bleu*100))


if __name__ == '__main__':
    pass