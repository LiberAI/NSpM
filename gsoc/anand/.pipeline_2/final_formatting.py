import sys
from tqdm import tqdm
import argparse
from sparql_generator import sparql_generator
# Given format #
# ['Property', 'Label ', 'Range', 'Fuzzy Score', 'Comment about expr', 'URI', 'Number of Occurrences', 'MVE', 'Optimal Expression', 'SPARQL Query Template', 'Generator Query\r\n']

# Required format : separated by semi-colon ##
# [ class_name, empty, empty, NLQ (MVE), Sparql Query, Generator Query] #


def final_formatting(input_file, uri_file, url, output_file, project_name, namespace,rs):
	
	if (int(rs) == 1) :
		open_files = open(input_file, 'r')
		lines = open_files.readlines()
		open_files.close()
	else:
		lines = sparql_generator(input_file=input_file, project_name=project_name,
									url=url, uri_file=uri_file, namespace=namespace)
	
	fl = 1

	output = ""

	"""
	- 	We iterate over the lines of the document.
	-	Convet the line into a list containig elements o the 
		string delimited by commas.
	-	
	"""
	for line in tqdm(lines):

		if fl:
			fl = 0
			continue
		l = line.split(',')

		# print l

		newl, to_remove = [], []
		name = url.split("/")[-1]
		newl.append("dbo:"+name)
		newl.append("")
		newl.append("")

		nlq = l[7].split()
		# The fuzzy score column is not present in the
		# autmatically created csv file.
		if(len(l) == 10):
			nlq = l[6].split()

		"""
		From MVE column a question is selected and each word
		is put into as an element of the list.
		"""
		for i in range(len(nlq)):
			if '(' in nlq[i] or ')' in nlq[i]:
				to_remove.append(nlq[i])
				continue
			if '<' not in nlq[i] and '?' not in nlq[i]:
				nlq[i] = nlq[i].lower()

		for x in to_remove:
			nlq.remove(x)

		spq = l[-2].split()
		"""
		Query one
		"""
		for i in range(len(spq)):
			if '<' not in spq[i] and '?' not in spq[i]:
				spq[i] = spq[i].lower()

		"""
		Query two
		"""
		gq = l[-1].split()
		for i in range(len(gq)):
			if '<' not in gq[i] and '?' not in gq[i] and '[' not in gq[i]:
				gq[i] = gq[i].lower()

		newl.append(" ".join(nlq))
		newl.append(" ".join(spq))
		newl.append(" ".join(gq))
		output += ";".join(newl) + "\n"

	fw = open(project_name+"/"+ output_file, 'w')
	fw.write(output)
	fw.close()


if __name__ == "__main__":
	"""
	Section to parse the command line arguments.
	"""
	parser = argparse.ArgumentParser()
	requiredNamed = parser.add_argument_group('Required Arguments')
	requiredNamed.add_argument('--input_file', dest='inp', metavar='inp',
								help='eg: File which contains metadata of properties', required=False)
	requiredNamed.add_argument(
		'--namespace', dest='ns', metavar='ns', help='eg: "ontology"', required=False)
	requiredNamed.add_argument('--output_file', dest='out', metavar='out',
								help='File in which you want to store output', required=False)
	requiredNamed.add_argument('--project_name', dest='project_name',
								metavar='project_name', help='test', required=False)
	requiredNamed.add_argument('--url', dest='url', metavar='url',
								help='Webpage URL: eg-http://mappings.dbpedia.org/server/ontology/classes/Place', required=False)
	requiredNamed.add_argument('--uri_file', dest='uri', metavar='uri',
								help='eg: File which contains uri and number of occurrences of properties', required=False)
	requiredNamed.add_argument('--rs', dest='rs', metavar='rs',
								help='Toggle to run separately', required=True)

	args = parser.parse_args()
	input_file = args.inp
	uri_file = args.uri
	url = args.url
	rs =args.rs
	namespace = args.ns
	output_file = args.out
	project_name = args.project_name
	final_formatting(input_file=input_file, uri_file=uri_file, url=url,
						output_file=output_file, project_name=project_name, namespace=namespace, rs= rs)
	pass
