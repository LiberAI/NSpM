import sys
f = open(sys.argv[1],'r')
lines = f.readlines()

for l in lines:
	l = l.split(',');
	if len(l) == 0:
		continue
	if l[5] == "" or len(l[5])==0:
		continue;
	if 'place' in l[2].lower() and l[5]!='':
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
		
		nlq = " ".join(nlq)
		
		spq = l[9].split();
		for i in range(len(spq)):
			if '<' not in spq[i] and '?' not in spq[i]:
				spq[i] = spq[i].lower()

		spq = " ".join(spq)
		

		gq = l[-1].split()
		for i in range(len(gq)):
			if '<' not in gq[i] and '?' not in gq[i] and '[' not in gq[i]: 
				gq[i] = gq[i].lower()

		gq = " ".join(gq)

		nlq = nlq.replace('<X>','<A>')
		spq = spq.replace('?x','?a').replace('<X>','<A>')
		gq = gq.replace('?x','?a').replace('<X>','<A>')
		newl.append((nlq))
		newl.append((spq))
		newl.append((gq))
		
		print ";".join(newl)