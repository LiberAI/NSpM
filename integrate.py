import sys

f = open(sys.argv[2],'r')
file = f.readlines()
d = {};

for l in file:
	l = l.strip().split('\t')
	d[l[0].split('/')[-1]] = l[1];

# print d["abstract"];


f = open(sys.argv[1],'r')
manual = f.readlines()
cnt,tot = 0,0;
final = ""

for m in manual:
	l = m.strip().split(',')
	m = l[0]
	tot += 1
	if m in d:
		cnt += 1;
		l.append("http://dbpedia.org/ontology/"+m)
		l.append(d[m])
	else:

		l.append('')
		l.append('')
		print m

	final += ",".join(l);
	final += '\n';

print final
f = open('manual-annotation-updated-v2.csv','w');
f.write(final);
print cnt, tot