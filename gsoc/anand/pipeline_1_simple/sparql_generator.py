import sys

"""
The code was changed at 41 and 42 to maintain the 
the structure of the intended output. 

The SPARQL needed 
to be saved for further purposes, which it wasn't initially
Section to parse the command line arguments.
"""

f = open(sys.argv[1],'r')


# print lines[0].split(',') 
# ['Property', 'Label ', 'Range', 'Fuzzy Score', 'Comment about expr', 'URI', 'Number of Occurrences', 
# 'MVE', 'Optimal Expression, SPARQL-TEMPLATE, GENERATOR-QUERY-TEMPLATE\r\n']
# sparql_template = []

"""
-	Read the file generated in the previous step.
-	Read the lines from the file an save it as a list.
-	If the frequency is known, Replace the 2nd last elemet of the formed list with
	a where statement, and last one witha where statement 
	followed by an assertion if it is a place.
-	Join the updated list with comma as a delimeter and save
	add it in the string ending with a newline character.
-	Print the final on the terminal
"""

lines = f.readlines()
final = ""
lineno = 1
for line in lines:
	if lineno == 1:
		lineno += 1
		continue
	line = line.strip().split(',')
	# print lines
	tem = 5
	if(len(line)==8):
		tem = 4
	print tem
	if line[tem]!='':
		# print line[5]
		# It was found the the MVE and OE was also required in output hence:
		#line[-2] = 'SELECT ?x WHERE { <X> <' + line[tem] + '> ?x }'
		#line[-1] = 'SELECT ?a WHERE { ?a <' + line[tem] + '> [] . ?a a <http://dbpedia.org/ontology/Place> }'
		line.append('SELECT ?x WHERE { <X> <' + line[tem] + '> ?x }')
		line.append('SELECT ?a WHERE { ?a <' + line[tem] + '> [] . ?a a <http://dbpedia.org/ontology/Place> }')


	final += ",".join(line)
	final += '\n'



# print final

# fw = open()

"""
This data generated might be required for further steps
thus it is saved in another file named sparql.csv
"""

open("sparql.csv",'w').write(final)



