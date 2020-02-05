import sys

f = open(sys.argv[1],'r')
# Given format #
# ['Property', 'Label ', 'Range', 'Fuzzy Score', 'Comment about expr', 'URI', 'Number of Occurrences', 'MVE', 'Optimal Expression', 'SPARQL Query Template', 'Generator Query\r\n']

# Required format : separated by semi-colon ##
# [ class_name, empty, empty, NLQ (MVE), Sparql Query, Generator Query] #

lines = f.readlines();
f.close()
fl = 1

output = ""
for line in lines:
	
	if fl:
		fl = 0
		continue
	l = line.split(',');
	# print l
	
	newl,to_remove = [],[]
	newl.append("dbo:Place")
	newl.append("")
	newl.append("")

	nlq = l[7].split();
	for i in range(len(nlq)):
		if '(' in nlq[i] or ')' in nlq[i]:
			to_remove.append(nlq[i]);
			continue
		if '<' not in nlq[i] and '?' not in nlq[i]:
			nlq[i] = nlq[i].lower()

	for x in to_remove:
		nlq.remove(x);

	spq = l[-2].split();
	for i in range(len(spq)):
		if '<' not in spq[i] and '?' not in spq[i]:
			spq[i] = spq[i].lower()

	gq = l[-1].split();
	for i in range(len(gq)):
		if '<' not in gq[i] and '?' not in gq[i] and '[' not in gq[i]: 
			gq[i] = gq[i].lower()

	newl.append(" ".join(nlq))
	newl.append(" ".join(spq))
	newl.append(" ".join(gq))
	output += ";".join(newl) + "\n";


fw = open(sys.argv[2],'w')
fw.write(output)
fw.close()