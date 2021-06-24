#!/usr/bin/env python
"""

Neural SPARQL Machines - Data generation.

'SPARQL as a Foreign Language' by Tommaso Soru and Edgard Marx et al., SEMANTiCS 2017
https://arxiv.org/abs/1708.07624

Version 2.0.0

"""
import argparse
import tensorflow as tf
from sklearn.model_selection import train_test_split

from prepare_dataset import load_dataset, convert


global output_direc


def merging_datafile(input_dir, output_dir):
    input_diren = input_dir + '/data.en'
    input_dirspq = input_dir + '/data.sparql'
    output_dir += '/data.txt'
    file1 = open(input_diren, 'r', encoding="utf8")
    Lines1 = file1.readlines()
    file2 = open(input_dirspq, 'r', encoding="utf8")
    Lines2 = file2.readlines()
    s = []
    for i in range(len(Lines1)):
        s.append(Lines1[i].replace('\n', " ") + "\t " + Lines2[i])

    filef = open(output_dir, 'w', encoding="utf8")
    filef.writelines(s)
    file1.close()
    file2.close()
    filef.close()
    return output_dir


def data_gen(input_dir, output_dir):

    output_direc = merging_datafile(input_dir, output_dir)

    input_tensor, target_tensor, inp_lang, targ_lang = load_dataset(output_direc)

    # Calculate max_length of the target tensors
    max_length_targ, max_length_inp = target_tensor.shape[1], input_tensor.shape[1]
    input_tensor_train, input_tensor_val, target_tensor_train, target_tensor_val = train_test_split(input_tensor, target_tensor, test_size=0.2)

    # Show length
    print(len(input_tensor_train), len(target_tensor_train), len(input_tensor_val), len(target_tensor_val))

    print("Input Language; index to word mapping")
    convert(inp_lang, input_tensor_train[0])
    print()
    print("Target Language; index to word mapping")
    convert(targ_lang, target_tensor_train[0])
    buffer_size = len(input_tensor_train)
    batch_size = 16
    steps_per_epoch = len(input_tensor_train) // batch_size
    embedding_dim = 256
    units = 1024
    vocab_inp_size = len(inp_lang.word_index) + 1
    vocab_tar_size = len(targ_lang.word_index) + 1

    dataset = tf.data.Dataset.from_tensor_slices((input_tensor_train, target_tensor_train)).shuffle(buffer_size)
    dataset = dataset.batch(batch_size, drop_remainder=True)
    example_input_batch, example_target_batch = next(iter(dataset))

    return dataset, vocab_inp_size, vocab_tar_size, embedding_dim, units, batch_size, example_input_batch, steps_per_epoch, targ_lang, max_length_targ, max_length_inp, inp_lang, targ_lang


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
    input_dir = args.input
    output_dir = args.output

    data_gen(input_dir, output_dir)
