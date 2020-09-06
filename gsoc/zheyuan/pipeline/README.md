
# One-Command Pipeline #
To run the complete pipeline, please use the command:

```bash
./pipeline.sh [$1 Project's name] [$2 Integer] [$3 Integer] [$4 Integer] [$5 Integer]
```
 $1 -- The project's name -- String -- Required
 $2 -- Dimension of the GloVe embeddings -- Integer [50|100|200|300] -- Optional, 300 by default
 $3 -- Number of unit in the LSTM cells -- Integer -- Optional, 512 by default
 $4 -- Training steps -- Integer -- Optional, 60000 by default
 $5 -- EXAMPLES_PER_TEMPLATE -- Integer -- Optional, 600 by default
Examples

```bash
./pipeline.sh Project1
```
```bash
./pipeline.sh Project2 300 512 60000 600
```


# Code Notes #
## Paraphrase Questions
After the creation of templates and the elimination of the never asked queries, the questions will be passed to the Paraphraser.
- `paraphrase_questions.py`: This aims to paraphrase the question template and return several possible candidates with their scores (potentially textual similarity, POS taggings, etc.). The main pipeline will select the templates with a strategy and add it/them to the template set.
- `textual_similarity.py`: This aims to calculate the scores of similarity between the candidates and the original question template.

To test the Paraphraser
```bash
python paraphrase_questions.py --sentence "what is your name ?"
```