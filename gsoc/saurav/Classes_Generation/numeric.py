from utils import read, get_properties_data

def categorize_numeric(data):
    
    # check for all simple questions and composite questions that contain number keyword
    final_data = []
    for sub_data in data:
        sub_data_split = sub_data.split(';')
        nlq = sub_data_split[3]
        p1 = sub_data_split[6]
        p2 = sub_data_split[7]
        if p1==p2 or "how" in nlq or "number" in nlq:
            final_data.append(sub_data)

    return final_data

def transform_sparql(sparql):
    
    index = sparql.index('where')
    query = 'select count(*) as ?x ' + sparql[index:] 

    return query

def refine_numeric(output_dir):
    
    data = read(output_dir+'/numeric/templates')
    quantitative_data = ["xsd:nonNegativeInteger", "Length", "xsd:integer", "xsd:float", "xsd:positiveInteger",  
                "Temperature", "Area", "Density", "Volume", "Currency", "Sales", "xsd:double", "Mass"]
    quantitative_data_date = ["xsd:gYear", "xsd:dateTime", "year", "xsd:date"] # no date type values
    dict_data = get_properties_data()
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
            if p1==p2:
                val = dict_data[p1].strip()
                if val in quantitative_data:
                    # quantitative peroperties
                    new_nlq = "How much is the " + p1 + " of <A> ?"
                elif val in quantitative_data_date:
                    pass
                else:
                    # !quantitative properties
                    new_nlq = "How many " + p1 + " did <A> have ?"
                    sub_data[4] = transform_sparql(sparql) # sparql query changes -> COUNT
            else:
                # remove 'number of' from property
                p1 = p1.replace("number of ", "")
                new_nlq = "How many " + p1.strip() + " did " + p2.strip() + " of <A> have ?"
        except:
            new_nlq = nlq

        if new_nlq != "":
            sub_data[3] = new_nlq
            sub_data = ';'.join(sub_data)
            final_data.append(sub_data)

    return final_data
