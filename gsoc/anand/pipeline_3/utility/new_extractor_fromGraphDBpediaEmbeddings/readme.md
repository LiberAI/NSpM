# SPARQL embedding extractor  
## With Significant decrease in time taken compared to older model: within ~1 minute.

- The code needs the big embedding file to be downloaded from the following link: [https://zenodo.org/record/1320038#.XT8CeHUzbEG](https://zenodo.org/record/1320038#.XT8CeHUzbEG)
- Run the following utility to make the process faster by breaking the files into smaller files. 
- If the files fail to load, then decrease the size of file in the script command. (breaker.sh)

The bash script:
```bash
echo "Creating data_fragments folder"
mkdir data_fragments
cd data_fragments
echo "Usage:    ./breaker.sh <size> <name of file to be split>" 
echo "Example:  ./breaker.sh 1000MB pageRank.txt"
echo "It will take some time, please remain calm." 
split -b $1  ../$2
```

## How to use? | Different components of this utility,
- For the utility to run the pageRank.txt files need to br present in this directory.
- First the `breaker.sh` script should be run as per the instructions stated above.
- After running the breaker.sh script run the following command on the terminal:
```bash
python indexer.py
```
- This will create an index for all the words present in the `pageRank.txt` file.
- After this we will require a vocab.sparql file which is the vocabulary (list of words for which you want to extract the embeddings.)
- Copy the vocab.sparql in this directory.
- Run the `embedding_extractor.py` code using the following command:
```bash
python embedding_extractor.py
```
- The new embeddings will be created with the name `new_vocabulary.csv`: which is an embedding file to be used in NMT. The file has the following format:
```
<word><space><n space sepeated values>
```

