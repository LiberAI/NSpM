from tqdm import tqdm
import numpy as np

def fetch_ranks(filename='../utility/wikidata.rank'):
    """
    The function loads rank from a supplied position.
    """
    sub = open(filename,'r').readlines()
    diction={}

    print("Loading Rankings")
    for val in tqdm(sub):
        diction[val.split('\t')[0]] = float(val.split('\t')[1])
    return diction

if __name__ == "__main__":
    fetch_ranks()
    pass

