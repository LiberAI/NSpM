#!/usr/bin/env bash
cd nmt
cat ../"$2" > to_ask.txt
python -m nmt.nmt  --vocab_prefix=../$1/vocab --model_dir=../$1_model  --inference_input_file=./to_ask.txt  --inference_output_file=./output.txt --out_dir=../$1_model --src=en --tgt=sparql | tail -n4
python ../analyse.py --target ../"$3" --generated output.txt > analysis.txt
cat analysis.txt
cd ..
