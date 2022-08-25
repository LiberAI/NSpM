import random
from utils import read, get_property

def categorize_con_disjunction(data, ontology):
    
    # check for all simple questions
    final_data = []
    for sub_data in data:
        sub_data_split = sub_data.split(';')
        nlq = sub_data_split[3]
        p1 = sub_data_split[6]
        p2 = sub_data_split[7]
        if p1==p2:
            final_data.append(sub_data)

    return final_data

def transform_sparql(sparql, p1, p2, ontology):
    
    # the structure changes s -> o, and o -> s plus 2 placeholders are added
    dict_data = get_property(ontology)
    try:
        query = 'select ?x where { <A> dbo:' + dict_data[p1] + ' ?x . <B> dbo:' + dict_data[p2] + ' ?x }'
    except:
        query = 'select ?x where { <A> dbo:' + p1 + ' ?x . <B> dbo:' + p2 + ' ?x }'

    return query

def refine_con_disjunction(output_dir, ontology):
    
    data = read(output_dir+'/con_disjunction/templates')
    terms = [" and ", " as well as "]
    final_data = []
    for sub_data in data:
        sub_data = sub_data.split(';')
        nlq = sub_data[3]
        sparql = sub_data[4]
        p1 = sub_data[6].strip()
        p2 = sub_data[7].strip()
        nlq_type = sub_data[-1].strip()
        new_nlq = ""

        # Replacing '<A>' with '<A>', and '<B>'
        rng = int(round(random.uniform(0,1)))
        term = "<A>" + terms[rng] + "<B>"
        new_nlq = nlq.replace("<A>", term)
        new_sparql = transform_sparql(sparql, p1, p2, ontology)

        sub_data[3] = new_nlq
        sub_data[4] = new_sparql
        sub_data = ';'.join(sub_data)
        final_data.append(sub_data)

    return final_data
