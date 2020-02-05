import sys
from decision_tree import decision_tree
import argparse
from tqdm import tqdm

"""
Section to parse the command line arguments.
"""

def sparql_generator(input_file, project_name, output_file="sparql_generator.csv", url="Use a valid URL", uri_file="Proper URI file", namespace="Valid namespace"):
	if __name__ == "__main__":
		f = open(input_file, 'r')
		lines = f.readlines()
		pass
	if not __name__ == "__main__":
		lines = decision_tree(input_file=input_file, project_name=project_name,
								url=url, uri_file=uri_file, namespace=namespace)
		pass

	# print lines[0].split(',')
	# ['Property', 'Label ', 'Range', 'Fuzzy Score', 'Comment about expr', 'URI', 'Number of Occurrences',
	# 'MVE', 'Optimal Expression, SPARQL-TEMPLATE, GENERATOR-QUERY-TEMPLATE\r\n']
	# sparql_template = []

	"""
	-	Read the file generated in the previous step.
	-	Read the lines from the file an save it as a list.
	-	If the frequency is known, Replace the 2nd last elemet of the formed list with
		a where statement, and last one witha where statement 
		followed by an assertion if it is a place.
	-	Join the updated list with comma as a delimeter and save
		add it in the string ending with a newline character.
	-	Print the final on the terminal
	"""
	accum = []
	final = ""
	lineno = 1
	for line in tqdm(lines):
		if lineno == 1:
			lineno += 1
			continue
		line = line.strip().split(',')
		# print lines
		if line[4] != '':
			# print line[5]
			# It was found the the MVE and OE was also required hence:
			#line[-2] = 'SELECT ?x WHERE { <X> <' + line[5] + '> ?x }'
			#line[-1] = 'SELECT ?a WHERE { ?a <' + line[5] + '> [] . ?a a <http://dbpedia.org/ontology/Place> }'
			line.append('SELECT ?x WHERE { <X> <' + line[4] + '> ?x }')
			line.append(
				'SELECT ?a WHERE { ?a <' + line[4] + '> [] . ?a a <http://dbpedia.org/ontology/Place> }')

		final += ",".join(line)
		accum.append(",".join(line))
		final += '\n'

	# print final

	# fw = open()

	"""
	This data generated might be required for further steps
	thus it is saved in another file named sparql.csv
	"""

	open(project_name+"/"+output_file, 'w').write(final)
	return accum


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
                               metavar='project_name', help='eg.:test', required=True)
    args = parser.parse_args()
    input_file = args.inp
    output_file = args.out
    project_name = args.project_name
    sparql_generator(input_file=input_file, output_file=output_file,
                     project_name=project_name)
    pass
