#!/usr/bin/env bash
cd nmt
echo "$2" > to_ask.txt
python -m nmt.nmt  --vocab_prefix=../$1/vocab --model_dir=../$1_model  --inference_input_file=./to_ask.txt  --inference_output_file=./output.txt --out_dir=../$1_model --src=en --tgt=sparql | tail -n4
echo ""
echo "ANSWER IN SPARQL SEQUENCE:"
cat output.txt
echo ""
cd ..
