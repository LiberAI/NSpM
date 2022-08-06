## Question Generator

1) Run pip installs

```
!pip install git+https://github.com/sauravjoshi23/Questgen.ai
!pip install sense2vec==1.0.3

!pip install git+https://github.com/boudinfl/pke.git

!python -m nltk.downloader universal_tagset
!python -m spacy download en

!wget https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz
!tar -xvf  s2v_reddit_2015_md.tar.gz
!ls s2v_old

!pip install constant
!pip install xmltodict
```

2) Change Line5 in usr/local/lib/python3.8/dist-packages/sense2vec/util.py -> from thinc.neural.util import get_array_module to from thinc.util import get_array_module  

3) Uncomment Line 2 and Lines 13-34 in usr/local/lib/python3.8/dist-packages/sense2vec/component.py 

4) Run 

```
!python "gsoc/saurav/Question_Generator/multi_generate_templates.py" --label "[Person]" --project_name "data/Person" --depth 2 --multi True
```

5) Pip install eliminator semantic similarity installations to eliminate templates that are not very efficient

```
!pip install transformers
!pip install sentence-transformers
!pip install nltk
```

6) Run

```
!python "gsoc/saurav/Question_Generator/eliminator.py" --input_file "data/Person/template_generator" --output_dir "data/Person" --threshold 0.40
```