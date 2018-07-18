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
	if len(line) == 0:
		continue
	if fl:
		fl = 0
		continue
	l = line.split(',');
	# print l
	if l[5] == "" or len(l[5])==0:
		continue;
	newl = []
	newl.append("dbo:Place")
	newl.append("")
	newl.append("")
	newl.append(l[7])
	newl.append(l[-2])
	newl.append(l[-1])
	output += ";".join(newl);


fw = open(sys.argv[2],'w')
fw.write(output)
fw.close()