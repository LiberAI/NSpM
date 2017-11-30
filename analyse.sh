#!/usr/bin/env bash

cd nmt
cat ../"$2" > to_ask.txt
python -m nmt.nmt  --vocab_prefix=../$1/vocab --model_dir=../$1_model  --inference_input_file=./to_ask.txt  --inference_output_file=./output.txt --out_dir=../$1_model --src=en --tgt=sparql | tail -n4

if [ $? -eq 0 ]
then
    cat output.txt > ../"$1"/output.txt
    python ../analyse.py --target ../"$3" --generated ../"$1"/output.txt > ../"$1"/analysis.txt

    if [ $? -eq 0 ]
    then
        cat ../"$1"/analysis.txt
    fi
fi
cd ..
