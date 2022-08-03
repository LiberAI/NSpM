
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

total = 0
classes = ['Airline', 'BodyOfWater', 'Bridge', 'EducationalInstitution', 'MusicalArtist', 'Olympics',
            'Organisation', 'Person_Work', 'WrittenWork'
    ]
name = ['subordinate', 'con_disjunction', 'comparative', 'superlative', 'numeric']

arr = []
for j in range(9):
    tot = 0
    for i in range(5):
        data = read('data/' + classes[j] + '/' + name[i] + '/paraphrased_templates')
        og = ""
        for sub_data in data:
            para = ""
            split_data = sub_data.split(';')
            # print(split_data)
            if split_data == [' ']:
                continue
            ontology = split_data[0]
            nlq = split_data[3]
            template_type = split_data[-1].strip()
            if template_type == 'Original' or template_type == 'QGen':
                og = nlq
            else:
                para = nlq

            if para != "":
                add = split_data
                add.insert(1, og)
                add = [i for i in add if i]
                add = ';'.join(add)
                arr.append(add)

print(len(arr))
write_data('gsoc/saurav/Elimination/combined_paraphrased_data', arr)

