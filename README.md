# 🤖 Neural SPARQL Machines

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

A Machine-Translation Approach for Question Answering over Knowledge Graphs.

![What does a NSpM do?](http://www.liberai.org/img/NSpM-image.png "What does a NSpM do?")

## IMPORTANT

If you are looking for the code for papers _"SPARQL as a Foreign Language"_ and _"Neural Machine Translation for Query Construction and Composition"_ please checkout tag [v0.1.0-akaha](https://github.com/LiberAI/NSpM/tree/v0.1.0-akaha) or branch [v1](https://github.com/LiberAI/NSpM/tree/v1).

## Install

### Via pip

Coming soon!

### Local setup

Clone the repository.

```bash
pip install -r requirements.txt
```

## Example of usage

### The Generator module

#### Pre-generated data

You can extract pre-generated data and model checkpoints from [here](https://nspm-models.s3.eu-west-2.amazonaws.com/v2/art_30.zip) (1.1 GB) in folders having the respective names.

#### Manual Generation (Alternative to using pre-generated data)

The template used in the paper can be found in a file such as `Annotations_F30_art.csv`. `data/art_30` will be the ID of the working dataset used throughout the tutorial. To generate the training data, launch the following command.

```bash
mkdir -p data/art_30
python generator.py --templates data/templates/Annotations_F30_art.csv --output data/art_30
```

Launch the command if you want to build dataset seprately else it will internally be called while training.

```bash
python data_gen.py --input data/art_30 --output data/art_30
```

### The Learner module

Now go back to the initial directory and launch `learner.py` to train the model. 

```bash
python learner.py --input data/art_30 --output data/art_30 --batch-size 32 --epochs 40
```

This command will create a model checkpoints in `data/art_30` and some pickle files in `data/art_30/pickle_objects`.

### The Interpreter module

Predict the SPARQL query for a given question it will store the detailed output in output_query.

```bash
python interpreter.py --input data/art_30 --output data/art_30 --inputstr "yuncken freeman has architected in how many cities?"
```
or, if you want to use [airml](https://github.com/sahandilshan/airML) to retrieve the model from KBox,
```bash
python interpreter.py --airml http://nspm.org/arts --output data/art_30 --inputstr "yuncken freeman has architected in how many cities?"
```

## Use cases & integrations

* Components of the [Adam Medical platform](https://www.graphen.ai/products/mi_feature.html) partly developed by [Jose A. Alvarado](https://www.linkedin.com/in/josealvaradoguzman/) at Graphen (including a humanoid robot called Dr Adam), rely on NSpM technology.
* The [Telegram NSpM chatbot](https://github.com/AKSW/NSpM/wiki/NSpM-Telegram-Bot) offers an integration of NSpM with the Telegram messaging platform.
* The [Google Summer of Code](https://summerofcode.withgoogle.com/) program has been supporting 6 students to work on NSpM-backed project "[A neural question answering model for DBpedia](https://github.com/dbpedia/neural-qa)" since 2018.
* A [question answering system](https://github.com/qasim9872/question-answering-system) was implemented on top of NSpM by [Muhammad Qasim](https://github.com/qasim9872).

## Publications

### SPARQL as a Foreign Language (2017)

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

### Neural Machine Translation for Query Construction and Composition (2018)

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

### Exploring Sequence-to-Sequence Models for SPARQL Pattern Composition (2020)

* arXiv: https://arxiv.org/abs/2010.10900

```
@inproceedings{panchbhai-2020,
    author = "Anand Panchbhai and Tommaso Soru and Edgard Marx",
    title = "Exploring Sequence-to-Sequence Models for {SPARQL} Pattern Composition",
    year = "2020",
    journal = "First Indo-American Knowledge Graph and Semantic Web Conference",
    url = "https://arxiv.org/abs/2010.10900",
}
```

### Liber AI on Medium (2020)

* [What is a Neural SPARQL Machine?](https://medium.com/liber-ai/what-is-a-neural-sparql-machine-c35945a5d278)

## Contact

### Questions?
* Primary contacts: [Tommaso Soru](http://tommaso-soru.it) and [Edgard Marx](http://emarx.org).
* Neural SPARQL Machines [mailing list](https://groups.google.com/forum/#!forum/neural-sparql-machines).
* Join the conversation on [Gitter](https://gitter.im/LiberAI/community).

### Follow us
* Follow the [project on ResearchGate](https://www.researchgate.net/project/Neural-SPARQL-Machines).
* Follow Liber AI Research on [Twitter](https://twitter.com/theLiberAI).

<p align="center"><img tooltip="Liber AI" src="http://www.liberai.org/img/Liber-AI-logo-name-200px.png" alt="Liber AI logo" border="0"></p>
