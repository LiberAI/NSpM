import json
from tqdm import tqdm
import sys

def json_extractor(file_name):
    csvfile = open(file_name,'r')
    if __name__ == "__main__":
        test_data = open("train-data-LCQuAD.csv",'w')
    ret_list = []
    with open(file_name) as f:
        data = json.load(f)

        for entity in tqdm(data):
            try:
                if __name__ == "__main__":
                    test_data.write(entity['corrected_question']+","+entity['sparql_query'] +","+entity['intermediary_question']+"\n")
            except:
                pass
            ret_list.append(  [entity['corrected_question'],entity['sparql_query'] ,entity['intermediary_question'] ]   )
    csvfile.close()
    if __name__ == "__main__":
        test_data.close()
    return ret_list


if __name__ == "__main__":
    json_extractor(sys.argv[1])
    pass

