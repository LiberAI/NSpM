#!/bin/bash

if [ ! -n "$1" ] ;then
    echo "you have not input a project name!"
else
    echo "The project name will be set to $1"


    # 1. Generate templates
    python multi_generate_templates.py --label '['Colour', 'Organisation', 'Person', 'Software', 'Artwork', 'Place', 'Work', 'Bird']' --project_name $1 --depth 1 --multi True

    # 2. Batch Paraphrasing
    # 2.1 Download BERT-Classifier

    model_dir="../utility/bert_classifier"
    if [ ! -d $model_dir ]; then
            curl --output $model_dir".zip" https://ndownloader.figshare.com/files/24431768\?private_link\=536ddbcfe3d805d7232f
            unzip $model_dir".zip" -d $model_dir

        else
            ls $model_dir/model_save2
    fi

    # 2.2 Launch Paraphraser
    python batch_paraphrase.py --templates ./$1/basic_sentence_and_template_generator --model $model_dir/model_save2/
    # 3. Generator
    # 3.1 Generate data.en/sparql
    cd ../../../  # [neural-qa]/gsoc/

    mkdir ./data/$1
    python generator.py --templates ./gsoc/zheyuan/pipeline/$1/basic_sentence_and_template_generator_paraphrased --output ./data/$1
    # 3.2 Generate vocab (simple tokenizing and normalization)
    cd ./gsoc/zheyuan/utility   # [neural-qa]/gsoc/zheyuan/utility
    python vocab_creator.py --path ../../../data/$1

    # 3.3 Generate Glove embeddings:

    #   3.3.1 Download GloVe 300d pretrained model
        if [ ! -d ./GloVe/glove.6B ]; then
            curl --output ./GloVe/glove.6B.zip http://downloads.cs.stanford.edu/nlp/data/glove.6B.zip

            unzip ./GloVe/glove.6B.zip -d ./Glove/glove.6B

          else
            ls ./GloVe/glove.6b
        fi

    #   3.3.2 Fine-tune en and Train sparql
    cd ./GloVe
    python glove_finetune.py --path ../../../../data/$1
    cd ./GloVe-master
    if [ "$(uname)"=="Darwin" ]; then
    # Mac OS X
      sed -i "" "s/CORPUS=.*/CORPUS=data_s.sparql/" demo.sh
      sed -i "" "s/SAVE_FILE=.*/SAVE_FILE=embed/" demo.sh
      sed -i "" "s/VECTOR_SIZE=.*/VECTOR_SIZE=300/" demo.sh
      sed -i "" "s/VOCAB_MIN_COUNT=.*/VOCAB_MIN_COUNT=1/" demo.sh
    elif [ "$(expr substr $(uname -s) 1 5)"=="Linux" ]; then
    # GNU/Linux
      sed -i "s/CORPUS=.*/CORPUS=data_s.sparql/" demo.sh
      sed -i "s/SAVE_FILE=.*/SAVE_FILE=embed/" demo.sh
      sed -i "s/VECTOR_SIZE=.*/VECTOR_SIZE=300/" demo.sh
      sed -i "s/VOCAB_MIN_COUNT=.*/VOCAB_MIN_COUNT=1/" demo.sh
    fi
    ./demo.sh
    cp ./embed.txt ../../../../../data/$1/embed.sparql

    # 4. NMT training
    # 4.1 Split into train/dev/test
    cd ../../../../../data/$1
    count=$(cat data.en |wc -l)
    echo $count "samples in total will be splitted into 8:1:1"
    python ../../split_in_train_dev_test.py --lines $count --dataset data.sparql
    cd ../../
    # 4.2 Training with embedding
    cd nmt
    python -m nmt.nmt --src=en --tgt=sparql --embed_prefix=../data/$1/embed --vocab_prefix=../data/$1/vocab --dev_prefix=../data/$1/dev --test_prefix=../data/$1/test --train_prefix=../data/$1/train --out_dir=../data/$1"_300d_model" --num_train_steps=60000 --steps_per_stats=100 --num_layers=2 --num_units=512 --dropout=0.2 --metrics=bleu,accuracy
    cd ..


fi