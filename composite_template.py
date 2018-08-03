import sys
f = open(sys.argv[1],'r')
lines = f.readlines()

# Given format #
# ['Property', 'Label ', 'Range', 'Fuzzy Score', 'Comment about expr', 'URI', 'Number of Occurrences', 'MVE', 'Optimal Expression', 'SPARQL Query Template', 'Generator Query\r\n']

# Required format : separated by semi-colon ##
# [ class_name, empty, empty, NLQ (MVE), Sparql Query, Generator Query] #
b = []
b.append("where is the")
b.append("")
b.append("of <A> located in")

for l in lines:
	l = l.strip().split(',')
	if len(l) == 0:
		continue
	if 'place' in l[2].lower() and l[5]!='' and len(l[5])!=0and 'location of' not in l[7].lower():
		
		newl,to_remove = [],[]
		newl.append("dbo:Place")
		newl.append("")
		newl.append("")

		l[1] = l[1].split()
		for i in range(len(l[1])):
			if '(' in l[1][i] or ')' in l[1][i]:
				to_remove.append(l[1][i]);
				continue
		for x in to_remove:
			l[1].remove(x);

		b[1] = " ".join(l[1])
		# print b
		nlq = " ".join(b)

		spq = "select ?a where { <A> " + l[5] + " ?b . ?b <http://dbpedia.org/ontology/location> ?a }"
		# print nlq + ";" + spq

		gq = l[-1]

		newl.append((nlq))
		newl.append((spq))
		newl.append((gq))
		newl = ";".join(newl)
		print newl