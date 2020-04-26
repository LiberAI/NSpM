from __future__ import print_function
import tensorflow as tf
import numpy as np
"""
- The following code when run with proper model location is capable of extracting the trained embeddings of a given model.
- The embeddings are present in the form: <word> <dimensions>
- The embedding decoder outputs sparql language embeddings
- The embedding encoder outputs english language embeddings
"""
def restore_session(self, session):
   saver = tf.train.import_meta_graph('./translate.ckpt-32000.meta')
   saver.restore(session, './translate.ckpt-32000')


def test_word2vec():
   opts = Options()    
   with tf.Graph().as_default(), tf.Session() as session:
       with tf.device("/cpu:0"):            
           model = Word2Vec(opts, session)
           model.restore_session(session)
           model.get_embedding("assistance")
accum = []
with tf.Session() as sess:
    saver = tf.train.import_meta_graph('translate.ckpt-32000.meta')
    print("***************")
    print(saver.restore(sess, "translate.ckpt-32000"))
    print(tf.all_variables())
    lis = (sess.run(('embeddings/decoder/embedding_decoder:0')))
    print(np.shape(lis))
    decode = open('vocab.sparql','r').readlines()
    embed = open('embed_vocab.sparql','w')
    if(len(decode) == np.shape(lis)[0]): 
        for dec in range(len(decode)):
            accum.append([decode[dec][:-1]]+list(lis[dec,:]))
            temp = ' '.join(str(v) for v in accum[-1])
            #print(temp)
            embed.write(temp+'\n')
    embed.close()
    

    lis = (sess.run(('embeddings/encoder/embedding_encoder:0')))
    print(np.shape(lis))
    decode = open('vocab.en','r').readlines()
    embed = open('embed_vocab.en','w')
    if(len(decode) == np.shape(lis)[0]): 
        for dec in range(len(decode)):
            accum.append([decode[dec][:-1]]+list(lis[dec,:]))
            temp = ' '.join(str(v) for v in accum[-1])
            #print(temp)
            embed.write(temp+'\n')
    embed.close()



    