import argparse

def merging_datafile(input_dir,output_dir):
    input_diren=input_dir+'/data.en'
    input_dirspq=input_dir+'/data.sparql'
    output_dir+='/data.txt'
    file1 = open(input_diren,'r',encoding="utf8")
    Lines1 = file1.readlines()
    file2 = open(input_dirspq,'r',encoding="utf8")
    Lines2 = file2.readlines()
    s=[]
    for i in range(len(Lines1)):
        s.append(Lines1[i].replace('\n'," ")+"\t "+Lines2[i])

    filef = open(output_dir,'w',encoding="utf8")
    filef.writelines(s)
    file1.close()
    file2.close()
    filef.close()
    return output_dir

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument(
        '--input', dest='input', metavar='inputDirectory', help='dataset directory', required=True)
    requiredNamed.add_argument(
        '--output', dest='output', metavar='outputDirectory', help='dataset directory', required=True)
    args = parser.parse_args()
    input_dir = args.input
    output_dir = args.output
    output_direc = merging_datafile(input_dir,output_dir)




    