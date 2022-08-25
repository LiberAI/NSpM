from utils import read

def categorize_subordinate(data, ontology):
    
    # check for both simple and composite questions 
    final_data = []
    for sub_data in data:
        nlq = sub_data.split(';')[3]
        final_data.append(sub_data)

    return final_data

def refine_subordinate(output_dir, ontology):
    
    data = read(output_dir+'/subordinate/templates')
    final_data = []
    for sub_data in data:
        sub_data = sub_data.split(';')
        nlq = sub_data[3]
        p1 = sub_data[6].strip()
        p2 = sub_data[7].strip()
        nlq_type = sub_data[-1].strip()
        new_nlq = ""
        try:
            # Original question
            if nlq_type == "Original": 
                if p1==p2: # Do nothing
                    new_nlq = nlq
                else: # Split by p2 index and transform later part
                    p2_index = nlq.index(p2)
                    f1 = nlq[:p2_index]
                    f2 = "<A>'s " + p2 + " ?"
                    new_nlq = f1 + f2
            # QGen question
            else:
                if p1==p2:
                    new_nlq = nlq
                else:
                    of_cnt = nlq.count(" of ")
                    if of_cnt == 2: # QGen = original with a very minor change -> What is the wheelbase of a vehicle of <A> ?
                        p2_index = nlq.index(p2)
                        f1 = nlq[:p2_index]
                        f2 = "<A>'s " + p2 + " ?"
                        new_nlq = f1 + f2
                    else: # QGen != Original major structure change -> What is the transmission of the <A> vehicle ?
                        new_nlq = nlq
        except:
            new_nlq = nlq

        sub_data[3] = new_nlq
        sub_data = ';'.join(sub_data)
        final_data.append(sub_data)

    return final_data
