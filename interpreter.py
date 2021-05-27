import tensorflow as tf
import argparse

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import numpy as np
import os
import pickle
from prepare_dataset import preprocess_sentence
from nmt import Encoder,Decoder
from generator_utils import decode, fix_URI

def evaluate(sentence):
  attention_plot = np.zeros((max_length_targ, max_length_inp))

  sentence = preprocess_sentence(sentence)

  inputs = [inp_lang.word_index[i] for i in sentence.split(' ')]
  inputs = tf.keras.preprocessing.sequence.pad_sequences([inputs],
                                                         maxlen=max_length_inp,
                                                         padding='post')
  inputs = tf.convert_to_tensor(inputs)

  result = ''

  hidden = [tf.zeros((1, units))]
  enc_out, enc_hidden = encoder(inputs, hidden)

  dec_hidden = enc_hidden
  dec_input = tf.expand_dims([targ_lang.word_index['<start>']], 0)

  for t in range(max_length_targ):
    predictions, dec_hidden, attention_weights = decoder(dec_input,
                                                         dec_hidden,
                                                         enc_out)

    # storing the attention weights to plot later on
    attention_weights = tf.reshape(attention_weights, (-1, ))
    attention_plot[t] = attention_weights.numpy()

    predicted_id = tf.argmax(predictions[0]).numpy()

    result += targ_lang.index_word[predicted_id] + ' '

    if targ_lang.index_word[predicted_id] == '<end>':
      return result, sentence, attention_plot

    # the predicted ID is fed back into the model
    dec_input = tf.expand_dims([predicted_id], 0)

  return result, sentence, attention_plot

def mkdir_p(mypath):
    '''Creates a directory. equivalent to using mkdir -p on the command line'''

    from errno import EEXIST
    from os import makedirs,path

    try:
        makedirs(mypath)
    except OSError as exc: # Python >2.5
        if exc.errno == EEXIST and path.isdir(mypath):
            pass
        else: raise

def plot_attention(attention, sentence, predicted_sentence,ou_dir):
  fig = plt.figure(figsize=(10,10))
  ax = fig.add_subplot(1, 1, 1)
  ax.matshow(attention, cmap='viridis')

  fontdict = {'fontsize': 14}

  ax.set_xticklabels([''] + sentence, fontdict=fontdict, rotation=90)
  ax.set_yticklabels([''] + predicted_sentence, fontdict=fontdict)

  ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
  ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

  plt.show()
  fig = plt.figure()
  mkdir_p(ou_dir)
  fig.savefig('{}/graph.png'.format(ou_dir))


def translate(sentence,ou_dir):
  result, sentence, attention_plot = evaluate(sentence)

  print('Input: %s' % (sentence))
  print('Predicted translation: {}'.format(result))

  attention_plot = attention_plot[:len(result.split(' ')), :len(sentence.split(' '))]
  plot_attention(attention_plot, sentence.split(' '), result.split(' '),ou_dir)
  return result



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument(
        '--input', dest='input', metavar='inputDirectory', help='dataset directory', required=True)
    requiredNamed.add_argument(
        '--output', dest='output', metavar='outputDirectory', help='dataset directory', required=True)
    requiredNamed.add_argument(
            '--inputstr', dest='inputstr', metavar='inputString', help='Input string for translation', required=False)

    args = parser.parse_args()
    inputs = args.inputstr
    model_dir = args.input
    input_dir = args.input
    model_dir+='/training_checkpoints'
    pic_dir=input_dir+'/pickle_objects'

    embedding_dim = 256
    units = 1024


    with open(pic_dir+'/input_tensor.pickle', 'rb') as f:
	    input_tensor=pickle.load(f)
    with open(pic_dir+'/target_tensor.pickle', 'rb') as f:
	    target_tensor=pickle.load(f)
    with open(pic_dir+'/inp_lang.pickle', 'rb') as f:
	    inp_lang=pickle.load(f)
    with open(pic_dir+'/targ_lang.pickle', 'rb') as f:
	    targ_lang=pickle.load(f)
    with open(pic_dir+'/BATCH_SIZE.pickle', 'rb') as f:
	    BATCH_SIZE=pickle.load(f)

    # Calculate max_length of the target tensors
    max_length_targ, max_length_inp = target_tensor.shape[1], input_tensor.shape[1]

    vocab_inp_size = len(inp_lang.word_index)+1
    vocab_tar_size = len(targ_lang.word_index)+1


    encoder = Encoder(vocab_inp_size, embedding_dim, units, BATCH_SIZE)
    decoder = Decoder(vocab_tar_size, embedding_dim, units, BATCH_SIZE)

    optimizer = tf.keras.optimizers.Adam()
    checkpoint = tf.train.Checkpoint(optimizer=optimizer,
                                 encoder=encoder,
                                 decoder=decoder)


    checkpoint.restore(tf.train.latest_checkpoint(model_dir))


    finaltrans = "input qurey : \n"
    finaltrans += inputs
    finaltrans += "\n \n \n output qurey : \n"
    finaltranso = translate(inputs,input_dir)
    finaltrans += finaltranso
    finaltrans += '\n \n \n output query decoded : \n'
    finaltranso = decode(finaltranso)
    finaltranso = fix_URI(finaltranso)
    print('Decoded translation: {}'.format(finaltranso))
    finaltrans += finaltranso
    outputfile = open((input_dir+'/output_query.txt'),'w',encoding="utf8")
    outputfile.writelines([finaltrans])
    outputfile.close()