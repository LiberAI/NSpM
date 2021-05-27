import argparse
import tensorflow as tf
import numpy as np
import os
import pickle
import time
from nmt import Encoder,Decoder,loss_function,BahdanauAttention
from sklearn.model_selection import train_test_split
from prepare_dataset import load_dataset,merging_datafile




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

def train(epochs,dir):
    model_dir = dir
    given_dir = model_dir+'/training_log.txt'
    model_dir+='/training_checkpoints'

    checkpoint_prefix = os.path.join(model_dir, "ckpt")
    EPOCHS = epochs
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument(
        '--input', dest='input', metavar='inputDirectory', help='dataset directory', required=True)
    requiredNamed.add_argument(
        '--output', dest='output', metavar='outputDirectory', help='dataset directory', required=True)
    requiredNamed.add_argument(
            '-BatchSize', dest='BatchSize',type=int, help='Input Batch Size for dataset according to data size', required=True)
    requiredNamed.add_argument(
            '-Epochs', dest='Epochs',type=int, help='Input string for translation', required=True)
    args = parser.parse_args()
    input_dir = args.input
    output_dir = args.output
    BATCH_SIZE = args.BatchSize
    Epoc=args.Epochs
    output_direc = merging_datafile(input_dir,output_dir)
    pic_dir=input_dir+'/pickle_objects'
    os.mkdir(pic_dir)

    num_examples = None
    input_tensor, target_tensor, inp_lang, targ_lang = load_dataset(output_direc, num_examples)
    max_length_targ, max_length_inp = target_tensor.shape[1], input_tensor.shape[1]
    input_tensor_train, input_tensor_val, target_tensor_train, target_tensor_val = train_test_split(input_tensor, target_tensor, test_size=0.2)

    BUFFER_SIZE = len(input_tensor_train)
    steps_per_epoch = len(input_tensor_train)//BATCH_SIZE
    embedding_dim = 256
    units = 1024
    vocab_inp_size = len(inp_lang.word_index)+1
    vocab_tar_size = len(targ_lang.word_index)+1

    dataset = tf.data.Dataset.from_tensor_slices((input_tensor_train, target_tensor_train)).shuffle(BUFFER_SIZE)
    dataset = dataset.batch(BATCH_SIZE, drop_remainder=True)
    example_input_batch, example_target_batch = next(iter(dataset))

    encoder = Encoder(vocab_inp_size, embedding_dim, units, BATCH_SIZE)
    decoder = Decoder(vocab_tar_size, embedding_dim, units, BATCH_SIZE)
    attention_layer = BahdanauAttention(10)
    sample_hidden = encoder.initialize_hidden_state()
    sample_output, sample_hidden = encoder(example_input_batch, sample_hidden)
    attention_result, attention_weights = attention_layer(sample_hidden, sample_output)

    optimizer = tf.keras.optimizers.Adam()
    checkpoint = tf.train.Checkpoint(optimizer=optimizer,
                                 encoder=encoder,
                                 decoder=decoder)

    
    with open(pic_dir+'/input_tensor.pickle', 'wb') as f:
	    pickle.dump(input_tensor, f)
    with open(pic_dir+'/target_tensor.pickle', 'wb') as f:
	    pickle.dump(target_tensor, f)
    with open(pic_dir+'/inp_lang.pickle', 'wb') as f:
	    pickle.dump(inp_lang, f)
    with open(pic_dir+'/targ_lang.pickle', 'wb') as f:
	    pickle.dump(targ_lang, f)
    with open(pic_dir+'/BATCH_SIZE.pickle', 'wb') as f:
	    pickle.dump(BATCH_SIZE, f)

    
    train(Epoc,input_dir)
    



