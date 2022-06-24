import random
from utils import read, get_properties_data

def categorize_superlative(data):
    
    # check for only composite questions that contain a quantitative secondary property and number keyword
    final_data = []
    quantitative_data = ["xsd:nonNegativeInteger", "Length", "xsd:integer", "xsd:float", "xsd:positiveInteger",  
                "Temperature", "xsd:gYear", "Area", "xsd:dateTime", "Density", "Volume", "Currency", 
                "year", "Sales", "xsd:double", "xsd:date", "Mass"]
    dict_data = get_properties_data()
    for sub_data in data:
        sub_data_split = sub_data.split(';')
        nlq = sub_data_split[3]
        p1 = sub_data_split[6] # secondary
        p2 = sub_data_split[7] # primary

        try:
            if p1!=p2 and "number" in nlq:
                final_data.append(sub_data)
            if p1!=p2:
                val = dict_data[p1].strip()
                if val in quantitative_data:
                    final_data.append(sub_data)                
        except:
            pass # key missing

    return final_data

def transform_sparql(sparql, num):

    terms = ["desc", "asc"]
    query = sparql + 'order by ' + terms[num] + '(?x) limit 1'
    
    return query

def refine_superlative(output_dir):
    
    data = read(output_dir+'/superlative/templates')
    terms = [["highest ", "largest "], ["lowest ", "smallest "]]
    final_data = []
    for sub_data in data:
        sub_data = sub_data.split(';')
        nlq = sub_data[3]
        sparql = sub_data[4]
        p1 = sub_data[6].strip()
        p2 = sub_data[7].strip()
        nlq_type = sub_data[-1].strip()
        new_nlq = ""
        try:
            rng_outer = int(round(random.uniform(0,1)))
            rng_inner = int(round(random.uniform(0,1)))
            term = terms[rng_outer][rng_inner]
            p1_index = nlq.index(p1)
            f1 = nlq[:p1_index]
            f2 = term + nlq[p1_index:]
            new_nlq = f1 + f2

            if rng_outer == 0:
                sparql = transform_sparql(sparql, 0)
            else:
                sparql = transform_sparql(sparql, 1)

            sub_data[3] = new_nlq
            sub_data[4] = sparql
            sub_data = ';'.join(sub_data)
            final_data.append(sub_data)
        except:
            pass

    return final_data
    