import sys, argparse
from tqdm import tqdm

"""
Section to parse the command line arguments.
"""

parser = argparse.ArgumentParser()
requiredNamed = parser.add_argument_group('Required Arguments')
requiredNamed.add_argument('--namespace', dest='ns', metavar='ns', help='eg: "ontology"', required=True)
requiredNamed.add_argument('--input_file', dest='inp', metavar='inp', help='eg: File which contains metadata of properties', required=True)
requiredNamed.add_argument('--uri_file', dest='uri', metavar='uri', help='eg: File which contains uri and number of occurrences of properties', required=True)
requiredNamed.add_argument('--output_file', dest='out', metavar='out', help='File in which you want to store output', required=True)
args = parser.parse_args()
namespace = args.ns

"""
How was the tsv file created in the first place?
- 	The tsv file is read.
- 	A dictionary diction in made.
-	Every time the namespace is matched with the name 
	space mentioned in the command line argument.
-	If the name space matches the dictionary diction here 
	is updated with {name of the entity = frequency of occurance}
"""

print("Reading the TSV file: ")
open_tsv = open(args.uri,'r')
read_tsv = open_tsv.readlines()
diction = {}

for line in tqdm(read_tsv):

	line = line.strip().split('\t')
	if line[0].split('/')[-2] != namespace:
		continue 
	diction[line[0].split('/')[-1]] = line[1]

open_tsv.close()
# print d["abstract"]

"""
Processing the input file. 
-	The input file is read, out put from get_properties.py
-	Reading lines from the input files.
-	Iterating over every line of the read file.
-	Taking the name from the line.
-	if the given name is in the dictionry created above 
	appending the url to the given name and corresponding 
	frequency to the row entry(read line). Else appending 
	an empty string. 
-	Joining all the elements of the list line with a comma,
	adding a new line character and then going for the next 
	iteration after adding it to a variable final (string addition)
"""
print("Reading the input file: ")
open_inp = open(args.inp,'r')
line_inp = open_inp.readlines()
cnt,tot = 0,0
final = ""

for in_line in tqdm(line_inp):
	line = in_line.strip().split(',')
	in_line = line[0]
	tot += 1
	# if ':' in m:
	# 	print "lol", m
	if in_line in diction:
		cnt += 1
		line.append("http://dbpedia.org/" + namespace + "/" +in_line)
		line.append(diction[in_line])
	else:

		line.append('')
		line.append('')
		#print in_line

	final += ",".join(line)
	final += '\n'

"""
The string final is the written to the output file name
as given in the command line argument.
"""
# print final
f = open(args.out,'w')
f.write(final)
print("**************************************")
print "Total number of entity whose URI was found: "+str(cnt) + "\nTotal number of entities present: " + str(tot)