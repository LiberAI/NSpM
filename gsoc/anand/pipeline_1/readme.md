# Automatic Training Data Generation For Neural QA Model

Follow the below given steps

## Steps to follow

### One - liner (For Steps 1-6)

Here is the skeleton of the command:
#### Make sure to use python3.7

``` bash
python final_formatting.py --rs <0 IF TO RUN THE WHOLE CODE | 1 TO RUN THE FUNTION OF THIS PYHTON SOURCE ONLY> --uri_file <URI FREQUENCY FILE TSV> --url <WEBPAGE URL> --output_file <OUTPUT FILE NAME > --project_name <PROJECT NAME> --namespace <NAMESPACE>
```

Example:

```bash
python final_formatting.py --rs 0 --uri_file ../uri_file_dbpedia-201610-properties.tsv --url http://mappings.dbpedia.org/server/ontology/classes/Place --output_file test_res.csv --project_name test --namespace ontology

```


### STEP 1 - Get properties from web page

Command:

```bash
python get_properties.py --url <WEBPAGE URL> --output_file <OUTPUT FILE NAME > --project_name <PROJECT NAME>
```

- `--url <WEBPAGE URL>`: --url argument is the webpage from where property metadata is to scraped example: http://mappings.dbpedia.org/server/ontology/classes/Place
- `--output_file <OUTPUT FILE NAME >`:  --output_file argument is the file where the output data of this function will be stored in CSV format.
- `--project_name <PROJECT NAME>`:  --project_name argument is the name given to the test case, a seperate folder with ths name will be ceated where the data files related to this project will be stored.

### STEP 2 - Get number of occurrences and URI

Store only the rows of required namespace properties

### STEP 3 - Integrate STEP 2 values with their corresponding property metadata row in temp.csv

Command:

``` bash
python integrate.py --uri_file <URI FREQUENCY FILE TSV> --input_file <OUTPUT FROM PREVIOUS STEP> --output_file <OUTPUT FILE> --project_name <PROJECT NAME> --namespace <NAMESPACE>
```

- `--uri_file <URI FREQUENCY FILE TSV>`: Files with frequency information
- `--input_file <OUTPUT FROM PREVIOUS STEP>`: Output file from previous step  
- `--output_file <OUTPUT FILE>` manual-annotation-updated-v2.csv (change it in the file if needed)
- `--namespace <NAMESPACE>` Change the namespace to the required (it is 'ontology' right now)
- `--project_name <PROJECT NAME>` Project Name

### STEP 4 - MVE generation

Command:

```bash
python decision_tree.py -input_file <OUTPUT FROM PREVIOUS STEP> --output_file <OUTPUT FILE> --project_name <PROJECT NAME>
```

- `--input_file <OUTPUT FROM PREVIOUS STEP>`: Output file from previous step  
- `--output_file <OUTPUT FILE>` Output file name
- `--project_name <PROJECT NAME>` Project Name

### STEP 5 - SPARQL Query Template and Generator Query generation

Command:

```bash
python sparql_generator.py -input_file <OUTPUT FROM PREVIOUS STEP> --output_file <OUTPUT FILE> --project_name <PROJECT NAME>
```

- `--input_file <OUTPUT FROM PREVIOUS STEP>`: Output file from previous step  
- `--output_file <OUTPUT FILE>` Output file name
- `--project_name <PROJECT NAME>` Project Name

### STEP 6 - Formatting the data into required format

Command:

Only run processes in this file and not the whole code:

```bash
python final_formatting.py --input_file <OUTPUT FROM PREVIOUS STEP> --rs <0 IF TO RUN THE WHOLE CODE | 1 TO RUN THE FUNTION OF THIS PYHTON SOURCE ONLY> --project_name <PROJECT NAME> --output_file <OUTPUT FILE>
```

Run the whole flow

```bash
python final_formatting.py --rs <0 IF TO RUN THE WHOLE CODE | 1 TO RUN THE FUNTION OF THIS PYHTON SOURCE ONLY> --uri_file <URI FREQUENCY FILE TSV> --url <WEBPAGE URL> --output_file <OUTPUT FILE NAME > --project_name <PROJECT NAME> --namespace <NAMESPACE>
```

- `--input_file <OUTPUT FROM PREVIOUS STEP>`: Output file from previous step  
- `--output_file <OUTPUT FILE>`: Output file name
- `--project_name <PROJECT NAME>`: Project Name
- `--uri_file <URI FREQUENCY FILE TSV>`: Files with frequency information
- `--namespace <NAMESPACE>`: Change the namespace to the required (it is 'ontology' right now)
- `--project_name <PROJECT NAME>`: Project Name
- `--rs <VALUE>`: 0 If To Run the whole code (whole flow) | 1 to run the function of this python source only

### STEP 7 - Follow the original data generation and training steps (readme of master branch)

Steps from the previous folder using the `test_res.csv` file for generator's template

## COMPOSITIONALITY EXPERIMENT

### One - liner

Here is the skeleton of the command:

``` bash
python composite_template.py --rs <0 IF TO RUN THE WHOLE CODE | 1 TO RUN THE FUNTION OF THIS PYHTON SOURCE ONLY> --uri_file <URI FREQUENCY FILE TSV> --url <WEBPAGE URL> --output_file <OUTPUT FILE NAME > --project_name <PROJECT NAME> --namespace <NAMESPACE>
```

Example:

```bash
python composite_template.py --rs 0 --uri_file ../uri_file_dbpedia-201610-properties.tsv --url http://mappings.dbpedia.org/server/ontology/classes/Place --output_file test_res.csv --project_name test --namespace ontology

```


### STEP 1 - Create template annotations (all a[i]'s)

Command:

```bash
python range_place.py -input_file <OUTPUT FROM PREVIOUS STEP> --output_file <OUTPUT FILE> --project_name <PROJECT NAME>
```

- `--input_file <OUTPUT FROM PREVIOUS STEP>`: Output file from previous step  
- `--output_file <OUTPUT FILE>` Output file name
- `--project_name <PROJECT NAME>` Project Name

### STEP 2 - Create composite templates (a[i]○b true for all i <= sizeof list 'a')

Command:

Only run processes in this file and not the whole code:

```bash
python composite_template.py --input_file <OUTPUT FROM PREVIOUS STEP> --rs <0 IF TO RUN THE WHOLE CODE | 1 TO RUN THE FUNTION OF THIS PYHTON SOURCE ONLY> --project_name <PROJECT NAME> --output_file <OUTPUT FILE>
```

Run the whole flow

```bash
python composite_template.py --rs <0 IF TO RUN THE WHOLE CODE | 1 TO RUN THE FUNTION OF THIS PYHTON SOURCE ONLY> --uri_file <URI FREQUENCY FILE TSV> --url <WEBPAGE URL> --output_file <OUTPUT FILE NAME > --project_name <PROJECT NAME> --namespace <NAMESPACE>
```

- `--input_file <OUTPUT FROM PREVIOUS STEP>`: Output file from previous step  
- `--output_file <OUTPUT FILE>`: Output file name
- `--project_name <PROJECT NAME>`: Project Name
- `--uri_file <URI FREQUENCY FILE TSV>`: Files with frequency information
- `--namespace <NAMESPACE>`: Change the namespace to the required (it is 'ontology' right now)
- `--project_name <PROJECT NAME>`: Project Name
- `--rs <VALUE>`: 0 If To Run the whole code (whole flow) | 1 to run the function of this python source only

### STEP 3 - Follow the original data generation and training steps (readme of master branch)

Steps from the previous folder.

### STEP 4 - Training

Choose any 10% templates and their output and shift it to new file (test data), rest of the contents of this file should be split into 90% train and 10% dev using the split_in_train_dev_test.py script

### STEP 5 - Run the training

Command:

```bash
sh train.sh <path of directory which contains train, dev and test data>
```
