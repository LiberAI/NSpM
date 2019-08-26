import sys
import re
import argparse
from tqdm import tqdm
from integrate import integrate


def decision_tree(input_file, project_name, output_file="decision_tree.csv", url="Use a valid URL", uri_file="Proper URI file", namespace="Valid namespace"):
    if __name__ == "__main__":
        f = open(input_file, 'r')
        lines = f.readlines()
        pass
    if not __name__ == "__main__":
        lines = integrate(namespace=namespace, uri_file=uri_file,
                          project_name=project_name, url=url)
    final_lines = []
    lineno = 1

    """ 
    print lines[0].split(',') 
    ['Property', 'Label ', 'Range', 'Fuzzy Score', 'Comment about expr', 'URI', 'Number of Occurrences', 
    'MVE', 'Optimal Expression\r\n']
    """

    """
    - 	The lines from the file generated in the previous steps
        is read and a for loop iterates through ecery row of 
    -	First we create a list of all elements seperated by commas.
    - 	If the range has the substring person, the we put as 
        question who else what.
    -	We append the question thus generate 2 times as minimum 
        viable instruction and optimal expression.
    - 	We create a variable names final lines and add strings,
        which are formed by adding strings formed by joining
        the elements of the list delemited by comma in each line.
    -	We also create a string of the question generated 
        delemited by a newline characte and store it in mve
        as a long string.
    - 	We output the series of question in mve_output.
    -	We save the final_lines strind in a file named GS_with_mve.csv
        delimeted by a newline character.
    """

    mve = ""
    for line in tqdm(lines):
        if lineno == 1:
            lineno += 1
            continue
        line = line.strip().split(',')
        rng = line[2].lower()
        lbl = line[1]
        if 'person' in rng:
            rng = "who"
        else:
            rng = "what"
        # The total length of a row in the list is 6,
        # thus 7 and 8 are out of range values. Thus I
        # replaced it with append.
        """ 
        line[7] = rng + " is the " + lbl + " of <X>"
        line[8] = rng + " is the " + lbl + " of <X>" 
        """
        if(len(line) < 9):
            line.append(rng + " is the " + lbl + " of <X>")
            line.append(rng + " is the " + lbl + " of <X>")
        else:
            line[7] = rng + " is the " + lbl + " of <X>"
            line[8] = rng + " is the " + lbl + " of <X>"
        mve += rng + " is the " + lbl + " of <X>\n"
        final_lines.append(",".join(line))

    fw = open(project_name+"/"+"mve"+output_file, 'w')
    fw.write(mve)

    fw2 = open(project_name+"/"+output_file, 'w')
    fw2.write("\n".join(final_lines))
    return final_lines

if __name__ == "__main__":
    """
    Section to parse the command line arguments.
    """
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')
    requiredNamed.add_argument('--input_file', dest='inp', metavar='inp',
                               help='Output from previous step', required=True)
    requiredNamed.add_argument('--output_file', dest='out', metavar='out',
                               help='File in which you want to store output', required=True)
    requiredNamed.add_argument('--project_name', dest='project_name',
                               metavar='project_name', help='test', required=True)
    args = parser.parse_args()
    input_file = args.inp
    output_file = args.out
    project_name = args.project_name
    decision_tree(input_file=input_file, output_file=output_file,
                  project_name=project_name)
    pass
