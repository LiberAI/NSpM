#!/usr/bin/env python
"""

Neural SPARQL Machines - Interpreter module.

'SPARQL as a Foreign Language' by Tommaso Soru and Edgard Marx et al., SEMANTiCS 2017
https://arxiv.org/abs/1708.07624

Version 2.0.0

"""
import os

# suppress tf and cuda messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

import argparse
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from tqdm import tqdm

from nmt import NeuralMT, NeuralMTConfig
from prepare_dataset import preprocess_sentence
from generator_utils import decode, fix_URI


def evaluate(sentence, config, neural_mt):

  max_length_targ, max_length_inp, inp_lang, targ_lang, units = config.max_length_targ, config.max_length_inp, config.inp_lang, config.targ_lang, config.units

  attention_plot = np.zeros((max_length_targ, max_length_inp))

  sentence = preprocess_sentence(sentence)

  # Handling OOV 
  inputs = []
  for i in sentence.split(' '):
    try:
      val = inp_lang.word_index[i]
      inputs.append(val)
    except:
      val = inp_lang.word_index['OOV']
      inputs.append(val)

  inputs = tf.keras.preprocessing.sequence.pad_sequences([inputs],
                                                         maxlen=max_length_inp,
                                                         padding='post')
  inputs = tf.convert_to_tensor(inputs)

  result = ''

  hidden = [tf.zeros((1, units))]
  enc_out, enc_hidden = neural_mt.encoder(inputs, hidden)

  dec_hidden = enc_hidden
  dec_input = tf.expand_dims([targ_lang.word_index['<start>']], 0)

  for t in range(max_length_targ):
    predictions, dec_hidden, attention_weights = neural_mt.decoder(dec_input,
                                                                   dec_hidden,
                                                                   enc_out)

    # storing the attention weights to plot later on
    attention_weights = tf.reshape(attention_weights, (-1, ))
    attention_plot[t] = attention_weights.numpy()

    predicted_id = tf.argmax(predictions[0]).numpy()

    result += targ_lang.index_word[predicted_id] + ' '

    if targ_lang.index_word[predicted_id] == '<end>':
      return result.strip(), sentence, attention_plot

    # the predicted ID is fed back into the model
    dec_input = tf.expand_dims([predicted_id], 0)

  return result.strip(), sentence, attention_plot


def mkdir_p(mypath):
  '''Creates a directory. equivalent to using mkdir -p on the command line'''

  from errno import EEXIST

  try:
    os.makedirs(mypath)
  except OSError as exc: # Python >2.5
    if exc.errno == EEXIST and os.path.isdir(mypath):
      pass
    else: raise


def plot_attention(attention, sentence, predicted_sentence, ou_dir, show_plot=False):
  fig = plt.figure(figsize=(10, 10))
  ax = fig.add_subplot(1, 1, 1)
  ax.matshow(attention, cmap='viridis') # [:-1,:-1]

  fontdict = {'fontsize': 14}

  ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
  ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

  ticks_loc_x = ax.get_xticks().tolist()
  ax.xaxis.set_major_locator(ticker.FixedLocator(ticks_loc_x))
  ticks_loc_y = ax.get_yticks().tolist()
  ax.yaxis.set_major_locator(ticker.FixedLocator(ticks_loc_y))

  print(sentence)
  print(predicted_sentence)

  ax.set_xticklabels([''] + sentence, fontdict=fontdict, rotation=90)
  ax.set_yticklabels([''] + predicted_sentence, fontdict=fontdict)

  mkdir_p(ou_dir)
  att_plot = f"{ou_dir}/attention.png"
  plt.savefig(att_plot)
  # print(f"Attention plot saved to: {att_plot}")
  if show_plot:
    plt.show()


def translate(sentence, ou_dir, config, neural_mt):
  result, sentence, attention_plot = evaluate(sentence, config, neural_mt)

  # print('Input: %s' % (sentence))
  # print('Predicted translation: {}'.format(result))

  # print(sentence.split(' '))
  # print(result.split(' '))

  print(attention_plot.shape)
  # attention_plot = attention_plot[:len(result.split(' ')), :len(sentence.split(' '))]
  # plot_attention(attention_plot, sentence.split(' '), result.split(' '), ou_dir)
  return result


def interpret(input_dir, queries):

  model_dir = input_dir
  model_dir += '/training_checkpoints'
  config = NeuralMT.load(input_dir)
  neural_mt = NeuralMT(config)
  checkpoint = neural_mt.checkpoint
  checkpoint.restore(tf.train.latest_checkpoint(model_dir)).expect_partial()

  sparql_queries = []
  for query in tqdm(queries):
    finaltrans = "input query: \n"
    finaltrans += query

    finaltrans += "\n \n \n output query: \n"
    finaltranso = translate(query, input_dir, config, neural_mt)
    finaltrans += finaltranso
    sparql_query = finaltranso

    finaltrans += '\n \n \n output query decoded: \n'
    finaltranso = decode(finaltranso)
    finaltranso = fix_URI(finaltranso)
    # print('Decoded translation: {}'.format(finaltranso))
    finaltrans += finaltranso

    # outputfile = open((input_dir + '/output_query.txt'), 'w', encoding="utf8")
    # outputfile.writelines([finaltrans])
    # outputfile.close()
    sparql_queries.append(sparql_query)

  return sparql_queries

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  requiredNamed = parser.add_argument_group('required named arguments')
  requiredNamed.add_argument(
      '--input', dest='input', metavar='inputDirectory', help='dataset directory', required=True)
  requiredNamed.add_argument(
          '--query', dest='query', metavar='query', help='Input query in natural language', required=True)

  args = parser.parse_args()
  input_dir = args.input
  query = args.query

  query = interpret(input_dir, [query])
  print("query: ", query)
