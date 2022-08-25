## Elimination

### Initial Elimination 

1) Run

```
!python "gsoc/saurav/Elimination/pair.py"
```

2) Run pip installs

```
!pip install transformers
!pip install sentence-transformers
!pip install nltk
```

3) Run

```
!python "gsoc/saurav/Elimination/initial_elimination.py" --input_file "gsoc/saurav/Elimination/combined_paraphrased_data" --output_dir "gsoc/saurav/Elimination" --threshold 0.90
```

### Commonsense Understanding

1) Run pip installs

```
!pip install transformers
!pip install sentence-transformers
!pip install sentencepiece
!pip install constant
!pip install wandb
```

2) Run

```
!python "gsoc/saurav/Elimination/commonsense.py" --input_dir "gsoc/saurav/Elimination/Commonsense_data/Training_data" --output_dir "gsoc/saurav/Elimination/Commonsense_data/Training_data"
```

```
!python "gsoc/saurav/Elimination/train.py" --category "commonsense" --train_path "gsoc/saurav/Elimination/Commonsense_data/Training_data/combined_train_data" --test_path "gsoc/saurav/Elimination/Commonsense_data/Test_data/test_data"
```

```
!python "gsoc/saurav/Elimination/classifier.py" --category "commonsense" --test_file "gsoc/saurav/Elimination/Commonsense_data/Test_data/test_data" --model_file "gsoc/saurav/Elimination/Model/commonsense_bert/commonsense_bert/bert_"
```

### Quora Question pairs task

1) Run

```
!python "gsoc/saurav/Elimination/train.py" --category "qq" --train_path "gsoc/saurav/Elimination/Quora_Question_Pairs_Dataset/Training_data/questions.csv" --test_path "gsoc/saurav/Elimination/Quora_Question_Pairs_Dataset/Test_data/test_data"
```

```
!python "gsoc/saurav/Elimination/classifier.py" --category "qq" --test_file "gsoc/saurav/Elimination/Quora_Question_Pairs_Dataset/Test_data/test_data" --model_file "gsoc/saurav/Elimination/Model/qq_bert/qq_bert/bert_"
```

### Final Select (Select the category of elimination method or None)

```
!python "gsoc/saurav/Elimination/final_select.py" --input_file "gsoc/saurav/Elimination/score_data" --output_file "gsoc/saurav/Elimination/final_template" --elimination "True" --elimination_type "commonsense" --model_file1 "gsoc/saurav/Elimination/Model/commonsense_bert/commonsense_bert/bert_"
```
```
!python "gsoc/saurav/Elimination/final_select.py" --input_file "gsoc/saurav/Elimination/score_data" --output_file "gsoc/saurav/Elimination/final_template" --elimination "True" --elimination_type "qq" --model_file1 "gsoc/saurav/Elimination/Model/qq_bert/qq_bert/bert_"
```
```
!python "gsoc/saurav/Elimination/final_select.py" --input_file "gsoc/saurav/Elimination/score_data" --output_file "gsoc/saurav/Elimination/final_template" --elimination "True" --elimination_type "both" --model_file1 "gsoc/saurav/Elimination/Model/commonsense_bert/commonsense_bert/bert_" --model_file2 "gsoc/saurav/Elimination/Model/qq_bert/qq_bert/bert_"
```
```
!python "gsoc/saurav/Elimination/final_select.py" --input_file "gsoc/saurav/Elimination/score_data" --output_file "gsoc/saurav/Elimination/final_template" --elimination "False"
```