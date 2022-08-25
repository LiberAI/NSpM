import os
import re

def read(input_file):
    file1 = open(input_file, 'r', encoding="utf8")
    Lines1 = file1.readlines()
    data = []
    for i in range(len(Lines1)):
        data.append(Lines1[i].replace('\n', " "))

    file1.close()
    return data

def write_data(output_file, data):

    output_file = open(output_file, 'w')
    for sub_data in data:
        output_file.write(sub_data+'\n')

def make_dir(directory):

  if not os.path.exists(directory):
    os.makedirs(directory)

def remove_bracket(question):

    r = re.compile(r'\([^)]*\)')
    r = re.sub(r, '', question)
    r = r.replace("  ", " ")
    return r

def get_properties_data(ontology):

    data = read('data/' +ontology+ '/get_properties.csv')
    dict_data = {}
    for i, row in enumerate(data):
        x = row.split(',')
        p = remove_bracket(x[1]).strip()
        dict_data[p] = x[3] # property label -> range value

    return dict_data


def get_property(ontology):

    data = read('data/' +ontology+ '/get_properties.csv')
    dict_data = {}
    for i, row in enumerate(data):
        x = row.split(',')
        p = remove_bracket(x[1]).strip()
        dict_data[p] = x[0] # property label -> property value
    
    return dict_data