import argparse
import tensorflow as tf
import numpy as np
import os
import io
import time
from nmt import *

@tf.function
def train_step(inp, targ, enc_hidden):
  loss = 0

  with tf.GradientTape() as tape:
    enc_output, enc_hidden = encoder(inp, enc_hidden)

    dec_hidden = enc_hidden

    dec_input = tf.expand_dims([targ_lang.word_index['<start>']] * BATCH_SIZE, 1)

    # Teacher forcing - feeding the target as the next input
    for t in range(1, targ.shape[1]):
      # passing enc_output to the decoder
      predictions, dec_hidden, _ = decoder(dec_input, dec_hidden, enc_output)

      loss += loss_function(targ[:, t], predictions)

      # using teacher forcing
      dec_input = tf.expand_dims(targ[:, t], 1)

  batch_loss = (loss / int(targ.shape[1]))

  variables = encoder.trainable_variables + decoder.trainable_variables

  gradients = tape.gradient(loss, variables)

  optimizer.apply_gradients(zip(gradients, variables))

  return batch_loss



'''parser = argparse.ArgumentParser()
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument(
    '--modeldir', dest='modeldir', metavar='modelDirectory', help='model directory', required=True)
args = parser.parse_args()'''
model_dir = input_dir
given_dir = model_dir+'/training_log.txt'
model_dir+='/training_checkpoints'

checkpoint_prefix = os.path.join(model_dir, "ckpt")
EPOCHS = 40
train_l=[]

for epoch in range(EPOCHS):
    empty_s=" "
    start = time.time()

    enc_hidden = encoder.initialize_hidden_state()
    total_loss = 0

    for (batch, (inp, targ)) in enumerate(dataset.take(steps_per_epoch)):
        batch_loss = train_step(inp, targ, enc_hidden)
        total_loss += batch_loss

        if batch % 100 == 0:
            print('Epoch {} Batch {} Loss {:.4f}'.format(epoch + 1,
                                                        batch,
                                                        batch_loss.numpy()))
    # saving (checkpoint) the model every 2 epochs
    if (epoch + 1) % 2 == 0:
        checkpoint.save(file_prefix = checkpoint_prefix)

    print('Epoch {} Loss {:.4f} \n'.format(epoch + 1,
                                        total_loss / steps_per_epoch))
    empty_s='Epoch {} Loss {:.4f} \n'.format(epoch + 1,
                                        total_loss / steps_per_epoch)
    print('Time taken for 1 epoch {} sec\n'.format(time.time() - start))
    empty_s+='Time taken for 1 epoch {} sec\n'.format(time.time() - start)
    train_l.append(empty_s)
filelog = open(given_dir,'w',encoding="utf8")
filelog.writelines(train_l)
filelog.close()
