import numpy as np
import argparse
from itertools import chain
from collections import Counter
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import ModelCheckpoint
import prepare_model
import infer


def return_data(file):
    texts = []
    with open(file, "rt") as myfile:
        for myline in myfile:
            myline = myline.strip()
            texts.append(myline)

    return texts


def return_subset(en, sp, ratio):
    size = (int(ratio*len(en)))
    en_sub = en[0:size]
    sp_sub = sp[0:size]

    if ratio <= 0.15:
        testsize = 0.15
    elif ratio <= 0.30:
        testsize = 0.12
    elif ratio <= 0.50:
        testsize = 0.1
    elif ratio <= 0.8:
        testsize = 0.05
    else:
        testsize = 0.005

    return en_sub, sp_sub, testsize


def _indexing(x, indices):
    """
    :param x: array from which indices has to be fetched
    :param indices: indices to be fetched
    :return: sub-array from given array and indices
    """
    # np array indexing
    if hasattr(x, 'shape'):
        return x[indices]

    # list indexing
    return [x[idx] for idx in indices]


def train_test_split(*arrays, test_size=0.25, shufffle=True, random_seed=1):
    """
    splits array into train and test data.
    :param arrays: arrays to split in train and test
    :param test_size: size of test set in range (0,1)
    :param shufffle: whether to shuffle arrays or not
    :param random_seed: random seed value
    :return: return 2*len(arrays) divided into train ans test
    """
    # checks
    assert 0 < test_size < 1
    assert len(arrays) > 0
    length = len(arrays[0])
    for i in arrays:
        assert len(i) == length

    n_test = int(np.ceil(length*test_size))
    n_train = length - n_test

    if shufffle:
        perm = np.random.RandomState(random_seed).permutation(length)
        test_indices = perm[:n_test]
        train_indices = perm[n_test:]
    else:
        train_indices = np.arange(n_train)
        test_indices = np.arange(n_train, length)

    return list(chain.from_iterable((_indexing(x, train_indices), _indexing(x, test_indices)) for x in arrays))

# fit a tokenizer


def create_tokenizer(lines):
    tokenizer = Tokenizer(
        filters='!"#$%&()*+,-./:;<=>?@[\\]^\'`{|}~\t\n')
    tokenizer.fit_on_texts(lines)
    return tokenizer

# max sentence length


def max_length(lines):
    return max(len(line.split()) for line in lines)

# encode and pad sequences


def encode_sequences(tokenizer, length, lines):
    # integer encode sequences
    X = tokenizer.texts_to_sequences(lines)
    # pad sequences with 0 values
    X = pad_sequences(X, maxlen=length, padding='post')
    return X


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="path to data")
    parser.add_argument(
        "ratio", type=float, help="Value 0-1 to represent the subset of original dataset")
    parser.add_argument("setsize", type=int, help="Count of datapoints for BackTranslation")
    

    args = parser.parse_args()
    en = args.path+'/data.en'
    sp = args.path+'/data.sparql'
    print('Preparing dataset for BackTranslation...')
    en_texts, sp_texts = return_data(en), return_data(sp)

    print('Creating {}% subset'.format(args.ratio*100))
    en_sub, sp_sub, testsize = return_subset(en_texts, sp_texts, args.ratio)
    en_sub_train, en_sub_test, sp_sub_train, sp_sub_test = train_test_split(
        en_sub, sp_sub, test_size=testsize)

    # prepare english tokenizer
    print('Preparing vocabulary for English questions.')
    eng_tokenizer = create_tokenizer(en_sub_train)
    eng_vocab_size = len(eng_tokenizer.word_index) + 1
    eng_length = max_length(en_sub_train)
    print('English Vocabulary Size: %d' % eng_vocab_size)
    print('English Max Length: %d' % (eng_length))

    # prepare sparql tokenizer
    print('Preparing vocabulary for SPAQRL questions.')
    spr_tokenizer = create_tokenizer(sp_sub_train)
    spr_vocab_size = len(spr_tokenizer.word_index) + 1
    spr_length = max_length(sp_sub_train)
    print('Sparql Vocabulary Size: %d' % spr_vocab_size)
    print('Sparql Max Length: %d' % (spr_length))

    print('Encoding sequences.')
    trainX = encode_sequences(spr_tokenizer, spr_length, sp_sub_train)
    trainY = encode_sequences(eng_tokenizer, eng_length, en_sub_train)

    testX = encode_sequences(spr_tokenizer, spr_length, sp_sub_test)
    testY = encode_sequences(eng_tokenizer, eng_length, en_sub_test)

    print('Data prepared.')

    # define model
    model = prepare_model.define_model(spr_vocab_size, eng_vocab_size, spr_length, eng_length, 256)
    model.compile(optimizer='Adam', loss='sparse_categorical_crossentropy')
    # summarize defined model
    print(model.summary())

    filename = 'spen_sub20.h5'
    checkpoint = ModelCheckpoint(filename, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
    model.fit(trainX, trainY, epochs=30, batch_size=64, validation_data=(testX, testY), callbacks=[checkpoint], verbose=True)


    print('Calculating bleu score for trained model.')
    #infer.bleuscore(model, eng_tokenizer, testX, en_sub_test)

    print('Preparing for Back-Translation')
    setsize = args.setsize
    en_original, sp_original = infer.randomset(en_sub_train, sp_sub_train, setsize)
    sp_infer = encode_sequences(spr_tokenizer, spr_length, sp_original)
    en_predicted = []
    batch = 256
    
    print('Back-Translating {} samples in batch size: {}'.format(args.setsize, batch))
    for i in range(int(len(en_original)/batch)):
        t, batch_predictions = infer.translate_batch(model, eng_tokenizer, sp_infer[(batch*i):(batch*(i+1))], en_original[(batch*i):(batch*(i+1))])
        for prediction in batch_predictions:
            en_predicted.append(prediction)

    print('Back-Translation complete, saving to directory {}'.format(args.path))
    sp_bt = open(args.path+'/bt.sparql', 'w')
    for s in sp_original:
        sp_bt.write(s + '\n')
    sp_bt.close()

    en_bt = open(args.path+'/bt.en', 'w')
    for e in en_predicted:
        en_bt.write(e + '\n')
    en_bt.close()