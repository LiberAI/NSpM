## Paraphraser

### Train

1) Run pip installations

```
!pip install transformers
!pip install constant
!pip install wandb
```

2) Run

```
!python gsoc/saurav/Paraphraser/bert_trainer.py --file_path gsoc/saurav/Paraphraser/Data/train.txt
```

### Inference

1) Run pip installs

```
!pip install transformers
!pip install sentencepiece
!pip install constant
!pip install wandb
```

2) Run

```
!python gsoc/saurav/Paraphraser/batch_paraphrase.py --templates data/Person/subordinate/refined_templates --output_file data/Person/subordinate/paraphrased_templates --model gsoc/saurav/Paraphraser/Model/albert-base-v2/albert-base-v2/albert-base-v2_ 
```
```
!python gsoc/saurav/Paraphraser/batch_paraphrase.py --templates data/Person/con_disjunction/refined_templates --output_file data/Person/con_disjunction/paraphrased_templates --model gsoc/saurav/Paraphraser/Model/albert-base-v2/albert-base-v2/albert-base-v2_
```
```
!python gsoc/saurav/Paraphraser/batch_paraphrase.py --templates data/Person/comparative/refined_templates --output_file data/Person/comparative/paraphrased_templates --model gsoc/saurav/Paraphraser/Model/albert-base-v2/albert-base-v2/albert-base-v2_
```
```
!python gsoc/saurav/Paraphraser/batch_paraphrase.py --templates data/Person/superlative/refined_templates --output_file data/Person/superlative/paraphrased_templates --model gsoc/saurav/Paraphraser/Model/albert-base-v2/albert-base-v2/albert-base-v2_
```
```
!python gsoc/saurav/Paraphraser/batch_paraphrase.py --templates data/Person/numeric/refined_templates --output_file data/Person/numeric/paraphrased_templates --model gsoc/saurav/Paraphraser/Model/albert-base-v2/albert-base-v2/albert-base-v2_
```