# Old and slow embedding extractor

- Please download the pageRank.txt file from the following link:  https://zenodo.org/record/1320038#.XT8CeHUzbEG.
- Run the extractor code in the following way:

```
For SPARQL: python sparql_extract_embed.py 
For English: python english_extract_embed.py 
```

## Note:

It works for file with the following format:
```
word<tab><n values seperated by tab>
word<tab><n values seperated by tab>
word<tab><n values seperated by tab>
word<tab><n values seperated by tab>
word<tab><n values seperated by tab>
word<tab><n values seperated by tab>
word<tab><n values seperated by tab>
word<tab><n values seperated by tab>
```

- The SPARQL prefixed python code replaces DBpedia urls with their shortforms like dbo, dbr.
- The en prefixed python code runs on the word without any modifications. 
