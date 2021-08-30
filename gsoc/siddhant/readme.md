## Google Summer of Code 2021 - DBpedia

### The Code folder contains all the work done through the coding period.

### To run and test the code, make sure to have all the dependencies from the requirements file installed.



### Work done : 

1. Syntax Aware Augmentation

to run the code,

```
cd gsoc/siddhant/DataAug/Syntax-aware
pip install -r requirements.txt

python augment.py
```

Involving dependency tree as a starting point this creates two pairs of augmented data, specifically for -Dropout and Replacement methods.

2. Back Translation

to run the code,

```
cd gsoc/siddhant/DataAug/BackTranslation
./pipeline.sh projectname ratio samplesize
```

Where 'path, ratio, samplesize size' are arguments needed to be passed for passed. For example,

```
./pipeline.sh BT1 0.20 2048
```

|parameters|passed|
|----------|------|
|projectname|BT1|
|ratio|0.20|
|samplesize|2048|

The pipeline prepares a subset of data with the **ratio** passed in as argument , trains a reverse translation model (Sparql->English) and then prepares a parallel text corpus of SPARQL as source and English questions as synthetic data.


### Future Scope

* Incorporating BERT to improve the NSpM for generating better translations for given English questions.
* Using the parallel data generated using the above techniques
* This data would help add robustness to noise 
* Using BERT as embeddings at a initial state
* Expecting a better translation performance 


For Detailed documentation checkout : [Blog](https://imsiddhant07.github.io/Neural-QA-Model-for-DBpedia/)