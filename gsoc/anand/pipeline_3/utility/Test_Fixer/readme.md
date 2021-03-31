# Dataset thresholder

This code creates a test set making sure the following constraints are 
followed: 
- The vocabulary in the test set has been learned in a separate context in the 
train set.
- Frequency Thresholding: The vocabulary in the test set is present in the train 
set for a given number of times.

To run the code, download the files from [here](https://nspm-models.s3.eu-west-2.amazonaws.com/misc/anand-pipeline_3-Test_Fixer-files.zip), then run the following command:

```python 
python text_fixer.py
```

Minimum requirements:

- `train.sparql` file containing the SPARQL queries of the training set.
- `old_test.sparql` The test set containing all the test SPARQL queries.
- `vocab.sparql` Vocabulary of the training set.

