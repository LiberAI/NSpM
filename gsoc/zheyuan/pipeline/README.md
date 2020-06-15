
# Pipeline #
To run please use the command:

```bash
python generate_templates.py --label <Ontology name : like Person, the casing matters > --project_name <Give a name to the project like test1 > --depth <Mention the depth to which you would like to penetrate: like 2 >
```

Example

```bash
python generate_templates.py --label Person --project_name test1 --depth 2
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