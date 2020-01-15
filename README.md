# 🤖 Neural SPARQL Machines
A LSTM-based Machine Translation Approach for Question Answering.

![British flag.](http://www.liberai.org/img/flag-uk-160px.png "English")
![Seq2Seq neural network.](http://www.liberai.org/img/seq2seq-webexport-160px.png "seq2seq")
![Semantic triple flag.](http://www.liberai.org/img/flag-sparql-160px.png "SPARQL")

This is a fork of the original repo which i updated to work with python3 and tensorflow 1.14.0

## Code

Install `git-lfs` in your machine, then fetch all files and submodules.

```bash
git lfs fetch
git lfs checkout
git submodule update --init
```

Install Python3.7 and TensorFlow (e.g., `sudo apt install python3 & pip install tensorflow==1.14.0`).

### Data preparation

#### Generation 

The template used in the paper can be found in a file such as `annotations_monument.tsv`. To generate the training data, launch the following command.

<!-- Made monument_300 directory in data directory due to absence of monument_300 folder in data directory  -->
```bash
mkdir data/monument_300
python generator.py --templates data/annotations_monument.csv  --output data/monument_300
```

Build the vocabularies for the two languages (i.e., English and SPARQL) with:

```bash
python build_vocab.py data/monument_300/data_300.en > data/monument_300/vocab.en
python build_vocab.py data/monument_300/data_300.sparql > data/monument_300/vocab.sparql
```

Count lines in `data_.*`
<!-- Fixing the bash related error pertaining to assigning value to NUMLINES here -->
```bash
NUMLINES=$(echo awk '{ print $1}' | cat data/monument_300/data_300.sparql |  wc -l)
echo $NUMLINES
# 7097
```

Split the `data_.*` files into `train_.*`, `dev_.*`, and `test_.*` (usually 80-10-10%).

<!-- Making this instruction consistent with the previous instructions by changing data.sparql to data_300.sparql -->
```bash
cd data/monument_300/
python ../../split_in_train_dev_test.py --lines $NUMLINES  --dataset data_300.sparql
```

#### Pre-generated data

Alternatively, you can extract pre-generated data from `data/monument_300.zip` and `data/monument_600.zip` in folders having the respective names.

### Training

<!-- Just a simple note to go back to the initial directory.-->
Now go back to the initail directory and launch `train.sh` to train the model. The first parameter is the prefix of the data directory and the second parameter is the number of training epochs.

```bash
sh train.sh data/monument_300 120000
```

This command will create a model directory called `data/monument_300_model`.

### Inference

Predict the SPARQL sentence for a given question with a given model.

```bash
sh ask.sh data/monument_300 "where is edward vii monument located in?"
 
```

### Chatbots, Integration & Cia

- Telegram: The [Telegram NSpM chatbot](https://github.com/AKSW/NSpM/wiki/NSpM-Telegram-Bot) offers an integration of NSpM with the Telegram message platform.

## Papers

### Soru and Marx et al., 2017

* Permanent URI: http://w3id.org/neural-sparql-machines/soru-marx-semantics2017.html
* arXiv: https://arxiv.org/abs/1708.07624

```
@inproceedings{soru-marx-2017,
    author = "Tommaso Soru and Edgard Marx and Diego Moussallem and Gustavo Publio and Andr\'e Valdestilhas and Diego Esteves and Ciro Baron Neto",
    title = "{SPARQL} as a Foreign Language",
    year = "2017",
    journal = "13th International Conference on Semantic Systems (SEMANTiCS 2017) - Posters and Demos",
    url = "http://w3id.org/neural-sparql-machines/soru-marx-semantics2017.html",
}
```

### Soru et al., 2018

* NAMPI Website: https://uclmr.github.io/nampi/
* arXiv: https://arxiv.org/abs/1806.10478

```
@inproceedings{soru-marx-nampi2018,
    author = "Tommaso Soru and Edgard Marx and Andr\'e Valdestilhas and Diego Esteves and Diego Moussallem and Gustavo Publio",
    title = "Neural Machine Translation for Query Construction and Composition",
    year = "2018",
    journal = "ICML Workshop on Neural Abstract Machines \& Program Induction (NAMPI v2)",
    url = "https://arxiv.org/abs/1806.10478",
}
```

## Contact

* Primary contacts: [Tommaso Soru](http://tommaso-soru.it) and [Edgard Marx](http://emarx.org).
* Neural SPARQL Machines [mailing list](https://groups.google.com/forum/#!forum/neural-sparql-machines).
* Follow the [project on ResearchGate](https://www.researchgate.net/project/Neural-SPARQL-Machines).
