#!/usr/bin/env bash
DATASET=$1

echo "Building English vocabulary..."
python build_vocab.py ${DATASET}/data.en > ${DATASET}/vocab.en
echo "Building SPARQL vocabulary..."
python build_vocab.py ${DATASET}/data.sparql > ${DATASET}/vocab.sparql

NUM_LINES=$(echo awk '{ print $1}' | cat ${DATASET}/data.sparql | wc -l)

NSPM_HOME=`pwd`
cd ${DATASET}
echo "Splitting data into train, dev, and test sets..."
python ${NSPM_HOME}/split_in_train_dev_test.py --lines $NUM_LINES --dataset data.sparql
cd ${NSPM_HOME}
echo "Done."
