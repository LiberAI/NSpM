# Compare SPARQL files 

The comparer will compare 2 files and determine the following:
- In a line by line inspection, how many lines were not exactly the same.
- A dictionary containing the number of errors in the matched lines like:
{
    0: 34044, 
    1: 36629, 
    2: 16682, 
    3: 4291, 
    7: 82, 
    8: 173, 
    11: 18, 
    12: 22, 
    'Wrong number of tokens': 22051
}
- To run the code please use the following:
```
python compare.py
```
Minimum requirements:
- `<file1>` and `<file2>` the 2 files to be compared. 