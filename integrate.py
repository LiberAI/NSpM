import sys, argparse

parser = argparse.ArgumentParser()
requiredNamed = parser.add_argument_group('Required Arguments');
requiredNamed.add_argument('--namespace', dest='ns', metavar='ns', help='eg: "ontology"', required=True)
requiredNamed.add_argument('--input_file', dest='inp', metavar='inp', help='eg: File which contains metadata of properties', required=True)
requiredNamed.add_argument('--uri_file', dest='uri', metavar='uri', help='eg: File which contains uri and number of occurrences of properties', required=True)
requiredNamed.add_argument('--output_file', dest='out', metavar='out', help='File in which you want to store output', required=True)
args = parser.parse_args()

namespace = args.ns

f = open(args.uri,'r')
file = f.readlines()
d = {};

for l in file:

	l = l.strip().split('\t')
	if l[0].split('/')[-2] != namespace:
		continue 
	d[l[0].split('/')[-1]] = l[1];

# print d["abstract"];


f = open(args.inp,'r')
manual = f.readlines()
cnt,tot = 0,0;
final = ""

for m in manual:
	l = m.strip().split(',')
	m = l[0]
	tot += 1
	# if ':' in m:
	# 	print "lol", m
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

# print final
f = open(args.out,'w');
f.write(final);
print cnt, tot