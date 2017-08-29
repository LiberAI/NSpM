# Neural SPARQL Machines
A LSTM-based Machine Translation Approach for Question Answering.

## Code

Fetch all files and submodules.

```bash
git lfs checkout
git submodule update
```

### Data generation

The template used in the paper can be found in file `annotations.tsv`. To generate the training data, launch the following command.

```bash
python generator.py
```

### Training

Launch `train.sh` to train the model. The first parameter is the prefix of the data directory. The second parameter is the number of training epochs.

```bash
sh train.sh data/monument_600 120000
```

This command will create a model directory called `data/monument_600_model`.

### Inference

Predict the SPARQL sentence for a given question with a given model.

```bash
sh ask.sh data/monument_600_model "where is edward vii monument located in?"
```

## Paper

* Permanent URI: http://w3id.org/neural-sparql-machines/soru-marx-semantics2017.html
* arXiv: https://arxiv.org/abs/1708.07624

## Cite

```
@proceedings{soru-marx-2017,
    author = "Tommaso Soru and Edgard Marx and Diego Moussallem and Gustavo Publio and Andr\'e Valdestilhas and Diego Esteves and Ciro Baron Neto",
    title = "{SPARQL} as a Foreign Language",
    year = "2017",
    journal = "13th International Conference on Semantic Systems (SEMANTiCS 2017) - Posters and Demos",
    url = "http://w3id.org/neural-sparql-machines/soru-marx-semantics2017.html",
}
```
