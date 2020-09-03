#!/bin/bash

# $1 -- The project's name -- String -- Required
# $2 -- Dimension of the GloVe embeddings -- Integer [50|100|200|300] -- Optional, 300 by default
# $3 -- Number of unit in the LSTM cells -- Integer -- Optional, 512 by default
# $4 -- Training steps -- Integer -- Optional, 60000 by default
# $5 -- EXAMPLES_PER_TEMPLATE -- Integer -- Optional, 600 by default

if [ ! -n "$1" ] ;then
    echo "you have not input a project name!"
else
    echo "The project name will be set to $1"

if [ ! -n "$2" ] ;then
    dimension=300
elif [[ ! $2 =~ ^[0-9]*$ ]]; then
    echo "Please enter an integer [50|100|200|300] to the second parameter to set the dimension of Glove Embeddings;"
    dimension=300
elif [ $2 -le 50 ]; then
    dimension=50
    echo "The dimension of GloVe embeddings is set to $dimension"
elif [ $2 -le 100 ]; then
    dimension=100
    echo "The dimension of GloVe embeddings is set to $dimension"
elif [ $2 -le 200 ]; then
    dimension=200
    echo "The dimension of GloVe embeddings is set to $dimension"
else
    dimension=300
    echo "The dimension of GloVe embeddings is set to $dimension"
fi
if [ ! -n "$3" ] ;then
    num_units=512
elif [[ ! $3 =~ ^[0-9]*$ ]]; then
    echo "Please enter an integer [ >=512 recommended ] to the third parameter to set the number of units of LSTM cells"
    num_units=512
else
    num_units=$3
    echo "The number of units of LSTM cells is set to $num_units"
fi
if [ ! -n "$4" ] ;then
    training_steps=60000
elif [[ ! $4 =~ ^[0-9]*$ ]]; then
    echo "Please enter an integer [ >=60000 recommended ] to the fourth parameter to set the number of training steps for Learner"
    training_steps=60000
else
    training_steps=$4
    echo "The number of training steps for Learner is set to $training_steps"
fi
if [ ! -n "$5" ] ;then
    examples_per_template=600
elif [[ ! $5 =~ ^[0-9]*$ ]]; then
    echo "Please enter an integer [ >=600 recommended ] to the fifth parameter to set the number of examples per template"
    examples_per_template=600
else
    examples_per_template=$5
    echo "The number of examples per template is set to $examples_per_template"
fi


    # 1. Generate templates
    partr="../utility/part-r-00000"

    if [ ! -d $partr ]; then
      wget https://s3.amazonaws.com/subjectiveEye/0.9/subjectiveEye3D/part-r-00000.gz
      gzip -d part-r-00000.gz
    fi
    python multi_generate_templates.py --label '['Agent', 'Place', 'Work', 'Species', 'TopicalConcept', 'MeanOfTransportation', 'Event', 'AnatomicalStructure', 'Device', 'TimePeriod', 'Activity']' --project_name $1 --depth 1 --multi True
#'['Agent', 'Place', 'Work', 'Species', 'TopicalConcept', 'MeanOfTransportation', 'Event', 'Algorithm', 'Altitude', 'AnatomicalStructure', 'Area', 'Award', 'Biomolecule', 'Blazon', 'Browser', 'ChartsPlacements', 'ChemicalSubstance', 'Cipher', 'Colour', 'Currency', 'Demographics', 'Depth', 'Device', 'Diploma', 'Disease', 'ElectionDiagram', 'ElectricalSubstation', 'EthnicGroup', 'FileSystem', 'Flag', 'Food', 'GeneLocation', 'GrossDomesticProduct', 'Holiday', 'Identifier', 'Language', 'List', 'Media', 'MedicalSpecialty', 'Medicine', 'Name', 'PersonFunction', 'Population', 'Protocol', 'PublicService', 'Relationship', 'PersonFunction', 'SportsSeason', 'Spreadsheet', 'StarCluster', 'Statistic', 'Tank', 'TimePeriod', 'UnitOfWork', 'Unknown']'
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
    python generator.py --templates ./gsoc/zheyuan/pipeline/$1/basic_sentence_and_template_generator_paraphrased --output ./data/$1 --examples $examples_per_template
    # 3.2 Generate vocab (simple tokenizing and normalization)
    cd ./gsoc/zheyuan/utility   # [neural-qa]/gsoc/zheyuan/utility
    python vocab_creator.py --path ../../../data/$1

    # 3.3 Generate Glove embeddings:

    #   3.3.1 Download GloVe 6B pretrained model
        if [ ! -d ./GloVe/glove.6B ]; then
            curl --output ./GloVe/glove.6B.zip http://downloads.cs.stanford.edu/nlp/data/glove.6B.zip

            unzip ./GloVe/glove.6B.zip -d ./GloVe/glove.6B

          else
            ls ./GloVe/glove.6b
        fi

    #   3.3.2 Fine-tune en and Train sparql
    cd ./GloVe
    python glove_finetune.py --path ../../../../data/$1
    cd ../../../../GloVe
    if [ "$(uname)" == "Darwin" ]; then
    # Mac OS X
      echo "This is a Mac OSX environment"
      sed -i "" "s/CORPUS=.*/CORPUS=data_s.sparql/" demo.sh
      sed -i "" "s/SAVE_FILE=.*/SAVE_FILE=embed/" demo.sh
      sed -i "" "s/VECTOR_SIZE=.*/VECTOR_SIZE=$dimension/" demo.sh
      sed -i "" "s/VOCAB_MIN_COUNT=.*/VOCAB_MIN_COUNT=1/" demo.sh
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then

    # GNU/Linux
      echo "This is a Linux environment"
      sed -i "s/CORPUS=.*/CORPUS=data_s.sparql/" demo.sh
      sed -i "s/SAVE_FILE=.*/SAVE_FILE=embed/" demo.sh
      sed -i "s/VECTOR_SIZE=.*/VECTOR_SIZE=$dimension/" demo.sh
      sed -i "s/VOCAB_MIN_COUNT=.*/VOCAB_MIN_COUNT=1/" demo.sh
    fi
    ./demo.sh
    cp ./embed.txt ../data/$1/embed.sparql

    # 4. NMT training
    # 4.1 Split into train/dev/test
    cd ../data/$1
    count=$(cat data.en |wc -l)
    echo $count "samples in total will be splitted into 8:1:1"
    python ../../split_in_train_dev_test.py --lines $count --dataset data.sparql
    cd ../../
    # 4.2 Training with embedding
    cd nmt
    python -m nmt.nmt --src=en --tgt=sparql --embed_prefix=../data/$1/embed --vocab_prefix=../data/$1/vocab --dev_prefix=../data/$1/dev --test_prefix=../data/$1/test --train_prefix=../data/$1/train --out_dir=../data/$1"_"$dimension"d_model" --num_train_steps=$training_steps --steps_per_stats=100 --num_layers=2 --num_units=$num_units --dropout=0.2 --metrics=bleu,accuracy
    cd ..

fi
