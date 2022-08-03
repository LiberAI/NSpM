import random
from utils import get_property, read, get_properties_data

def categorize_comparative(data, ontology):
    
    # check for all simple questions and only composite questions that contain a quantitative secondary property and number keyword
    final_data = []
    quantitative_data = ["xsd:nonNegativeInteger", "Length", "xsd:integer", "xsd:float", "xsd:positiveInteger",  
                "Temperature", "xsd:gYear", "Area", "xsd:dateTime", "Density", "Volume", "Currency", 
                "year", "Sales", "xsd:double", "xsd:date", "Mass"]
    dict_data = get_properties_data(ontology)
    for sub_data in data:
        sub_data_split = sub_data.split(';')
        nlq = sub_data_split[3]
        p1 = sub_data_split[6] # secondary
        p2 = sub_data_split[7] # primary

        try:
            if p1==p2: 
                final_data.append(sub_data)
            elif "number" in nlq:
                final_data.append(sub_data)
            else:
                val = dict_data[p1].strip()
                if val in quantitative_data:
                    final_data.append(sub_data)
        except:
            pass # key missing

    return final_data

def transform_sparql(sparql, num, p2, symbol, value, ontology):
    
    query = ""
    if num == 1:
        index = sparql.index('{')
        add = sparql[index:]
        query = 'ask where ' + add
    elif num == 2:
        dict_data = get_property(ontology)
        try:
            query = 'ask where { <B> dbo:' + dict_data[p2] + ' <A> }'
        except:
            query = 'ask where { <B> dbo:' + p2 + ' <A> }'
    elif num == 3:
        mid_change = '?x1 dbo:' + p2 + ' <A> '
        aft = sparql[sparql.index('.'):]
        sparql = 'select ?x where { ' + mid_change + aft
        add = 'filter ( ?x ' + symbol + ' ' + value + ') }'
        query = sparql.replace('}', add)

    return query

def refine_comparative(output_dir, ontology):
    
    data = read(output_dir+'/comparative/templates')
    final_data = []
    for sub_data in data:
        sub_data = sub_data.split(';')
        nlq = sub_data[3]
        sparql = sub_data[4]
        p1 = sub_data[6].strip()
        p2 = sub_data[7].strip()
        nlq_type = sub_data[-1].strip()
        new_nlq = ""

        if p1 == p2:

            # Type 1
            new_nlq1 = "Did <A> have " + p2 + " ?"
            sub_data[3] = new_nlq1
            sparql = transform_sparql(sparql, 1, p2, None, None, ontology)
            sub_data[4] = sparql
            sub_data = ';'.join(sub_data)
            final_data.append(sub_data)

            # Type 2
            sub_data = sub_data.split(';')
            new_nlq2 = "Is <A> " + p2 + " of <B> ?"
            sub_data[3] = new_nlq2
            sparql = transform_sparql(sparql, 2, p2, None, None, ontology)
            sub_data[4] = sparql
            sub_data = ';'.join(sub_data)
            final_data.append(sub_data)
        else:
            
            terms = ["more than ", "less than "]
            symbols = [">", "<"]
            numeric_terms = ["1 ", "10 ", "100 ", "5 ", "50 ", "500 "]
            rng1 = int(round(random.uniform(0,1)))
            rng2 = int(round(random.uniform(0,5)))

            new_nlq = "Give me all " + p2.strip() + " of <A> with " + terms[rng1] + numeric_terms[rng2] + p1 + " ?"
            sub_data[3] = new_nlq
            sparql = transform_sparql(sparql, 3, p2, symbols[rng1], numeric_terms[rng2], ontology)
            sub_data[4] = sparql
            sub_data = ';'.join(sub_data)
            final_data.append(sub_data)        

    return final_data
