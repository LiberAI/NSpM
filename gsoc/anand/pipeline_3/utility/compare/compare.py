""" 
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
"""

from tqdm import tqdm

ref = open("test.sparql",'r').readlines()
test = open("output_test",'r').readlines()
diction_error = {}
counter = 0
for val in tqdm(range(len(ref))):
    error_count = 0
    ref_s = ref[val].split(" ")
    test_s = test[val].split(" ")
    """ print("```")
    print("reference:"+ref[val])
    print("test:"+test[val])
    print("```") """
    if (ref_s != test_s):
        counter+=1
    try:
        for count in range(len(ref_s)):
            if(ref_s[count] == test_s[count]):
                continue
            else:
                error_count += 1
                #print("ref:"+ref_s[count]+"</br>")
                #print("test:"+test_s[count]+"</br>")
    except:
        error_count = "Wrong number of tokens"
        #print("Wrong number of tokens")
    if(error_count not in diction_error.keys()):
        diction_error[(error_count)] = 1
    diction_error[(error_count)] += 1
    #print("\n----\n")
print(counter)
print(diction_error)