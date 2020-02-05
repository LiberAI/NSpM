import sys
import argparse
import os
from  sparql_generator import sparql_generator
from tqdm import tqdm

def range_place(input_file, project_name, output_file="test_res.csv", url="Use a valid URL", uri_file="Proper URI file", namespace="Valid namespace"):
    if __name__ == "__main__":
        f = open(input_file, 'r')
        lines = f.readlines()
        f.close()
        print ("hello")
    if not __name__ == "__main__":
        lines = sparql_generator(input_file=input_file, project_name=project_name,
                                    url=url, uri_file=uri_file, namespace=namespace)

    output_file_write = open(project_name+"/" + output_file, 'w')
    name = url.split("/")[-1]
    accum = []
    for l in tqdm(lines):
        l = l.split(',')
        if len(l) == 0:
            continue
        if l[5] == "" or len(l[5]) == 0:
            continue
        if name.lower() in l[2].lower() and l[5] != '':
            newl, to_remove = [], []
            newl.append("dbo:"+name)
            newl.append("")
            newl.append("")
            nlq = l[7].split()
            for i in range(len(nlq)):
                if '(' in nlq[i] or ')' in nlq[i]:
                    to_remove.append(nlq[i])
                    continue
                if '<' not in nlq[i] and '?' not in nlq[i]:
                    nlq[i] = nlq[i].lower()

            for x in to_remove:
                nlq.remove(x)

            nlq = " ".join(nlq)

            spq = l[9].split()
            for i in range(len(spq)):
                if '<' not in spq[i] and '?' not in spq[i]:
                    spq[i] = spq[i].lower()

            spq = " ".join(spq)

            gq = l[-1].split()
            for i in range(len(gq)):
                if '<' not in gq[i] and '?' not in gq[i] and '[' not in gq[i]:
                    gq[i] = gq[i].lower()

            gq = " ".join(gq)

            nlq = nlq.replace('<X>', '<A>')
            spq = spq.replace('?x', '?a').replace('<X>', '<A>')
            gq = gq.replace('?x', '?a').replace('<X>', '<A>')
            newl.append((nlq))
            newl.append((spq))
            newl.append((gq))
            accum.append(";".join(newl))
    output_file_write.write("\n".join(accum))
    return [lines,output_file_write]


if __name__ == "__main__":
    """
    Section to parse the command line arguments.
    """
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')
    requiredNamed.add_argument('--input_file', dest='inp', metavar='inp',
                               help='eg: File which contains metadata of properties', required=True)
    requiredNamed.add_argument('--output_file', dest='out', metavar='out',
                               help='File in which you want to store output', required=True)
    requiredNamed.add_argument('--project_name', dest='project_name',
                               metavar='project_name', help='test', required=True)
    requiredNamed.add_argument('--url', dest='url', metavar='url',
								help='Webpage URL: eg-http://mappings.dbpedia.org/server/ontology/classes/Place', required=True)
	
    args = parser.parse_args()
    input_file = args.inp
    output_file = args.out
    url = args.url
    project_name = args.project_name
    range_place(input_file=input_file, output_file=output_file,
                project_name=project_name, url=url)
