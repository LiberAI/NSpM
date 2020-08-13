import math, argparse
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import os
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('universal_tagset')
from nltk import pos_tag, word_tokenize, RegexpParser

from constant import Constant
const = Constant()
const.MODULE_URL = "https://tfhub.dev/google/universal-sentence-encoder-large/5" #@param ["https://tfhub.dev/google/universal-sentence-encoder/2", "https://tfhub.dev/google/universal-sentence-encoder-large/3"]
# os.environ['TFHUB_CACHE_DIR'] = '/tmp/tfhub_modules'
print('start')
embed = hub.load(const.MODULE_URL)

def similarities(sentence, paraphrases):
    vectors = embed([sentence] + paraphrases)
    cosine_similarities = []
    for v2 in vectors[1:]:
        cosine_similarities.append(cosine_similarity(np.array(vectors[0]), np.array(v2)))

    return cosine_similarities

def similarity(sentence,paraphrase):
    vectors = embed([sentence, paraphrase])
    return cosine_similarity(vectors[0], vectors[1])

# def cosine_similarities(v1, vectors):
#     #Calculate semantic similarity between two original v1 and paraphrased vectors
#     similarities = []
#     for v2 in vectors:
#         similarities.append(cosine_similarity(v1,v2))
#     return similarities


def cosine_similarity(v1, v2):
    # Calculate semantic similarity between two sentence vectors
    mag1 = np.linalg.norm(v1)
    mag2 = np.linalg.norm(v2)
    if (not mag1) or (not mag2):
        return 0
    return np.dot(v1, v2) / (mag1 * mag2)


def prof_similarity(v1, v2):
    #Calculate the semantic similarity based on the angular distance
    cosine = cosine_similarity(v1, v2)
    prof_similarity = 1 - math.acos(cosine) / math.pi
    return prof_similarity

def minDistance(s1, s2):
    """
    :type s1: str
    :type s2: str
    :rtype: int
    """

    len1 = len(s1)
    len2 = len(s2)
    dp = [[0 for _ in range(len2 + 1)] for _ in range(len1 + 1)]
    for i in range(len1 + 1):
        for j in range(len2 + 1):
            if i > 0 and j == 0:
                dp[i][j] = dp[i - 1][j] + 1
            elif j > 0 and i == 0:
                dp[i][j] = dp[i][j - 1] + 1
            elif j > 0 and i > 0:
                res1 = dp[i - 1][j] + 1
                res2 = dp[i][j - 1] + 1
                res3 = not s1[i - 1] == s2[j - 1] and dp[i - 1][j - 1] + 1 or dp[i - 1][j - 1]
                dp[i][j] = min(res1, res2, res3)
    return dp[len1][len2]


def words_distance(sentence1, sentence2):
    return minDistance(word_tokenize(sentence1), word_tokenize(sentence2))


def tags_distance(sentence1, sentence2):
    tagged1 = pos_tag(word_tokenize(sentence1), tagset='universal')
    tagged2 = pos_tag(word_tokenize(sentence2), tagset='universal')
    tags1 = [j for i, j in tagged1]
    tags2 = [j for i, j in tagged2]
    return minDistance(tags1, tags2)


from collections import Counter

def count_NNP(sentence):
    tokens = word_tokenize(sentence)
    tagged = pos_tag(tokens)
    tag = [j for i, j in tagged]
    result = Counter(tag)
    return result["NNP"]

def has_NNP(sentence, num):
    tokens = word_tokenize(sentence)
    tagged = pos_tag(tokens)
    tag = [j for i, j in tagged]
    result = Counter(tag)
    return result["NNP"] <= num



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--s1', dest='sentence1', metavar='sentence1',
                               help='a sentence', required=True)
    requiredNamed.add_argument('--s2', dest='sentence2', metavar='sentence2',
                               help='another sentence', required=True)
    args = parser.parse_args()
    s1 = args.sentence1
    s2 = args.sentence2
    print("cosine similarity:", similarity(s1, s2), "Edit distance: ", edit_distance(s1,s2))
    pass
