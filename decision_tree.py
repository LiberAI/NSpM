import sys, re

f = open(sys.argv[1],'r')
lines = f.readlines();

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
		rng = "Who"
	else:
		rng = "What"
	mve += rng + " is the " + lbl + " of <X>\n" 

fw = open('data/mve_output','w')
fw.write(mve)

