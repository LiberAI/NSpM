# 🤖 Neural SPARQL Machines

A LSTM-based Machine Translation Approach for Question Answering over Knowledge Graphs.

![British flag.](http://www.liberai.org/img/flag-uk-160px.png "English")
![Seq2Seq neural network.](http://www.liberai.org/img/seq2seq-webexport-160px.png "seq2seq")
![Semantic triple flag.](http://www.liberai.org/img/flag-sparql-160px.png "SPARQL")


## Code

Install `git-lfs` in your machine, then fetch all files and submodules.

```bash
git lfs fetch
git lfs checkout
git submodule update --init
```

### Python setup

Codebase: Python 3.7+

```bash
pip install -r requirements.txt
```

### The Generator module

#### Pre-generated data

You can extract pre-generated data from `data/monument_300.zip` and `data/monument_600.zip` in folders having the respective names.

#### Manual Generation (Alternative to using pre-generated data)

The template used in the paper can be found in a file such as `annotations_monument.tsv`. `data/monument_300` will be the ID of the working dataset used throughout the tutorial. To generate the training data, launch the following command.

<!-- Made monument_300 directory in data directory due to absence of monument_300 folder in data directory  -->
```bash
mkdir data/monument_300
python generator.py --templates data/annotations_monument.csv --output data/monument_300
```

Launch the command to build the vocabularies for the two languages (i.e., English and SPARQL) and split into train, dev, and test sets.

```bash
./generate.sh data/monument_300
```

### The Learner module

<!-- Just a simple note to go back to the initial directory.-->
Now go back to the initial directory and launch `train.sh` to train the model. The first parameter is the prefix of the data directory and the second parameter is the number of training epochs.

```bash
./train.sh data/monument_300 12000
```

This command will create a model directory called `data/monument_300_model`.

### The Interpreter module

Predict the SPARQL sentence for a given question with a given model.

```bash
./ask.sh data/monument_300 "where is edward vii monument located in?"
```

## Use cases & Integrations

* [The Telegram NSpM chatbot](https://github.com/AKSW/NSpM/wiki/NSpM-Telegram-Bot) offers an integration of NSpM with the Telegram messaging platform.

## Papers

### Soru and Marx et al., 2017

* arXiv: https://arxiv.org/abs/1708.07624

```
@inproceedings{soru-marx-2017,
    author = "Tommaso Soru and Edgard Marx and Diego Moussallem and Gustavo Publio and Andr\'e Valdestilhas and Diego Esteves and Ciro Baron Neto",
    title = "{SPARQL} as a Foreign Language",
    year = "2017",
    journal = "13th International Conference on Semantic Systems (SEMANTiCS 2017) - Posters and Demos",
    url = "https://arxiv.org/abs/1708.07624",
}
```

### Soru et al., 2018

* NAMPI Website: https://uclnlp.github.io/nampi/
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
* Follow [Liber AI Research](http://liberai.org) on [Twitter](https://twitter.com/theLiberAI).

![Liber AI logo.](http://www.liberai.org/img/Liber-AI-logo-name-200px.png "Liber AI")
