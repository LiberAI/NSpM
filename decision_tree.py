import sys, re

f = open(sys.argv[1],'r')
lines = f.readlines();
final_lines = []

lineno = 1

# print lines[0].split(',') 
# ['Property', 'Label ', 'Range', 'Fuzzy Score', 'Comment about expr', 'URI', 'Number of Occurrences', 
# 'MVE', 'Optimal Expression\r\n']

mve = ""
for line in lines:
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
	line[7] = rng + " is the " + lbl + " of <X>"
	line[8] = rng + " is the " + lbl + " of <X>"
	mve += rng + " is the " + lbl + " of <X>\n"
	final_lines.append(",".join(line));


fw = open('data/mve_output','w')
fw.write(mve)

fw2 = open('GS_with_mve.csv','w');
fw2.write("\n".join(final_lines))

