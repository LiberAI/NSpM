import sys
from range_place import range_place
import argparse
from tqdm import tqdm

# RUN: python composite_template.py data/GS-v3.csv
# Given format #
# ['Property', 'Label ', 'Range', 'Fuzzy Score', 'Comment about expr', 'URI', 'Number of Occurrences', 'MVE', 'Optimal Expression', 'SPARQL Query Template', 'Generator Query\r\n']

# Required format : separated by semi-colon ##
# [ class_name, empty, empty, NLQ (MVE), Sparql Query, Generator Query] #

def composite_template(input_file, uri_file, url, output_file, project_name, namespace,rs):
	if (int(rs) == 1) :
		open_files = open(input_file, 'r')
		lines = open_files.readlines()
		open_files.close()
		output_file_write = open(project_name+"/" + output_file, 'w')
	else:
		list_val = range_place(input_file=input_file, project_name=project_name,
									url=url, uri_file=uri_file, namespace=namespace)
		lines = list_val[0]
		output_file_write = list_val[1]

	
	b = []
	b.append("where is the")
	b.append("")
	b.append("of <A> located in")
	accum = []
	for l in tqdm(lines):
		l = l.strip().split(',')
		# print l
		if len(l) == 0:
			continue
		if 'place' in l[2].lower() and l[5]!='' and len(l[5])!=0 and 'location of' not in l[7].lower():
			
			newl,to_remove = [],[]
			newl.append("dbo:Place")
			newl.append("")
			newl.append("")

			l[1] = l[1].split()
			for i in range(len(l[1])):
				if '(' in l[1][i] or ')' in l[1][i]:
					to_remove.append(l[1][i])
					continue
			for x in to_remove:
				l[1].remove(x)

			b[1] = " ".join(l[1])
			# print b
			nlq = " ".join(b)
			# no Fuzzy score so the index decreases by 1
			spq = "select ?a where { <A> " + l[4] + " ?b . ?b <http://dbpedia.org/ontology/location> ?a }"
			# print nlq + ";" + spq

			gq = l[-1]

			gq2 = gq.split()[1]
			gq2 = "distinct(" + gq2 + ")"
			gq = gq.split()
			gq[1] = gq2
			gq = " ".join(gq).replace("SELECT","select").replace("WHERE","where")


			newl.append((nlq))
			newl.append((spq))
			newl.append((gq))
			newl = ";".join(newl)
			accum.append(newl)
	output_file_write.write("\n")
	output_file_write.write("\n".join(accum))
	output_file_write.close()


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
	composite_template(input_file=input_file, uri_file=uri_file, url=url,
						output_file=output_file, project_name=project_name, namespace=namespace, rs= rs)
	pass