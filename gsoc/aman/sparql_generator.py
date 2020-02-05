import sys

f = open(sys.argv[1],'r')
lines = f.readlines();

# print lines[0].split(',') 
# ['Property', 'Label ', 'Range', 'Fuzzy Score', 'Comment about expr', 'URI', 'Number of Occurrences', 
# 'MVE', 'Optimal Expression, SPARQL-TEMPLATE, GENERATOR-QUERY-TEMPLATE\r\n']
# sparql_template = []

final = ""
lineno = 1
for line in lines:
	if lineno == 1:
		lineno += 1
		continue
	line = line.strip().split(',')
	# print lines
	if line[5]!='':
		# print line[5]
		line[-2] = 'SELECT ?x WHERE { <X> <' + line[5] + '> ?x }'
		line[-1] = 'SELECT ?a WHERE { ?a <' + line[5] + '> [] . ?a a <http://dbpedia.org/ontology/Place> }'

	final += ",".join(line)
	final += '\n'


print final
# fw = open()


