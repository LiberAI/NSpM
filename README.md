# 🤖 Neural SPARQL Machines
A LSTM-based Machine Translation Approach for Question Answering.

![alt text](http://www.liberai.org/img/flag-uk-160px.png "English")
![alt text](http://www.liberai.org/img/seq2seq-webexport-160px.png "seq2seq")
![alt text](http://www.liberai.org/img/flag-sparql-160px.png "SPARQL")

## Code

Install `git-lfs` in your machine, then fetch all files and submodules.

```bash
git lfs fetch
git lfs checkout
git submodule update --init
```

Install TensorFlow (e.g., `pip install tensorflow`).

### Data preparation

#### Generation 

The template used in the paper can be found in a file such as `annotations_monument.tsv`. To generate the training data, launch the following command.

```bash
python generator.py --templates data/annotations_monument.csv  --output data/monument_300
```

Build the vocabularies for the two languages (i.e., English and SPARQL) with:

```bash
python build_vocab.py data/monument_300/data_300.en > data/monument_300/vocab.en
python build_vocab.py data/monument_300/data_300.sparql > data/monument_300/vocab.sparql
```

Count lines in `data_.*`
```bash
NUMLINES= $(echo awk '{ print $1}' | cat data/monument_300/data_300.sparql |  wc -l)
echo $NUMLINES
# 7097
```

Split the `data_.*` files into `train_.*`, `dev_.*`, and `test_.*` (usually 80-10-10%).
```bash
cd data/monument_300/
python ../../split_in_train_dev_test.py --lines $NUMLINES  --dataset data.sparql
```

#### Pre-generated data

Alternatively, you can extract pre-generated data from `data/monument_300.zip` and `data/monument_600.zip` in folders having the respective names.

### Training

Launch `train.sh` to train the model. The first parameter is the prefix of the data directory. The second parameter is the number of training epochs.

```bash
sh train.sh data/monument_300 120000
```

This command will create a model directory called `data/monument_300_model`.

### Inference

Predict the SPARQL sentence for a given question with a given model.

```bash
sh ask.sh data/monument_300 "where is edward vii monument located in?"
```

## Paper

* Permanent URI: http://w3id.org/neural-sparql-machines/soru-marx-semantics2017.html
* arXiv: https://arxiv.org/abs/1708.07624

```
@proceedings{soru-marx-2017,
    author = "Tommaso Soru and Edgard Marx and Diego Moussallem and Gustavo Publio and Andr\'e Valdestilhas and Diego Esteves and Ciro Baron Neto",
    title = "{SPARQL} as a Foreign Language",
    year = "2017",
    journal = "13th International Conference on Semantic Systems (SEMANTiCS 2017) - Posters and Demos",
    url = "http://w3id.org/neural-sparql-machines/soru-marx-semantics2017.html",
}
```

## Contact

* Neural SPARQL Machines [mailing list](https://groups.google.com/forum/#!forum/neural-sparql-machines).
* Follow the [project on ResearchGate](https://www.researchgate.net/project/Neural-SPARQL-Machines).
