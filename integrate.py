import sys

parser = argparse.ArgumentParser()
requiredNamed = parser.add_argument_group('Required Arguments');
requiredNamed.add_argument('--namespace', dest='ns', metavar='ns', help='eg: "ontology"', required=True)
requiredNamed.add_argument('--output_file', dest='out', metavar='out', help='File in which you want to store output', required=True)
args = parser.parse_args()

namespace = args.ns

f = open(sys.argv[2],'r')
file = f.readlines()
d = {};

for l in file:

	l = l.strip().split('\t')
	if l[0].split('/')[-2] != namespace:
		continue 
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
		l.append("http://dbpedia.org/" + namespace + "/" +m)
		l.append(d[m])
	else:

		l.append('')
		l.append('')
		print m

	final += ",".join(l);
	final += '\n';

print final
f = open(args.out,'w');
f.write(final);
print cnt, tot