import math
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

from constant import Constant
const = Constant()
const.MODULE_URL = "https://tfhub.dev/google/universal-sentence-encoder-large/3" #@param ["https://tfhub.dev/google/universal-sentence-encoder/2", "https://tfhub.dev/google/universal-sentence-encoder-large/3"]

embed = hub.Module(const.MODULE_URL)

def similarity(sentence1, sentence2):
  texts = [sentence1, sentence2]
  with tf.Session() as sess:
    sess.run([tf.global_variables_initializer(), tf.tables_initializer()])

    vectors = sess.run(embed(texts))
    cosine_similarities = cosine_similarity(vectors[0],vectors[1])


    return cosine_similarities

def cosine_similarity(v1, v2):
    #Calculate semantic similarity between two
    mag1 = np.linalg.norm(v1)
    mag2 = np.linalg.norm(v2)
    if (not mag1) or (not mag2):
        return 0
    return np.dot(v1, v2) / (mag1 * mag2)



def prof_similarity(v1, v2):
    cosine_similarity = cosine_similarity(v1, v2)
    prof_similarity = 1 - math.acos(cosine_similarity) / math.pi
    return prof_similarity