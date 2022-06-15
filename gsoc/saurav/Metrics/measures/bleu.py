import numpy as np
from nltk.translate.bleu_score import sentence_bleu

def bleu(target, predicted):
    scores = []
    for i in range(len(target)):
        val = sentence_bleu([target[i].split()], predicted[i].split(), weights=(0.25, 0.25, 0.25, 0.25))
        scores.append(val)

    scores = np.array(scores)
    bleu_score = np.mean(scores)
    print('bleu score for given model {}'.format(bleu_score*100))
