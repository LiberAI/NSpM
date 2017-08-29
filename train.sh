#!/usr/bin/env bash
~/anaconda2/bin/python -m nmt.nmt --src=en --tgt=sparql --vocab_prefix=$1/vocab --dev_prefix=$1/dev --test_prefix=$1/test --train_prefix=$1/train --out_dir=$1_model --num_train_steps=$2 --steps_per_stats=100 --num_layers=2 --num_units=128 --dropout=0.2 --metrics=bleu
