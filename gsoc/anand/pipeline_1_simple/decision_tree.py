import sys, re

"""
Was updated at line 61 and 62, could not take the intput from
the previous step as input. 
Section to parse the command line arguments.
"""

f = open(sys.argv[1],'r')
lines = f.readlines()
final_lines = []

lineno = 1



""" 
print lines[0].split(',') 
['Property', 'Label ', 'Range', 'Fuzzy Score', 'Comment about expr', 'URI', 'Number of Occurrences', 
 'MVE', 'Optimal Expression\r\n']
"""

"""
- 	The lines from the file generated in the previous steps
	is read and a for loop iterates through every row.
-	First we create a list of all elements seperated by commas.
- 	If the range has the substring person, the we put as 
	question who else what.
-	We append the question thus generate 2 times as minimum 
	viable instruction and optimal expression.
- 	We create a variable names final lines and add strings,
	which are formed by adding strings formed by joining
	the elements of the list delemited by comma in each line.
-	We also create a string of the question generated 
	delemited by a newline characte and store it in mve
	as a long string.
- 	We output the series of question in mve_output.
-	We save the final_lines strind in a file named GS_with_mve.csv
	delimeted by a newline character.
"""

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
	# The total length of a row in the list is 6, 
	# thus 7 and 8 are out of range values. Thus I
	# replaced it with append.
	""" 
	line[7] = rng + " is the " + lbl + " of <X>"
	line[8] = rng + " is the " + lbl + " of <X>" 
	"""
	line.append(rng + " is the " + lbl + " of <X>")
	line.append(rng + " is the " + lbl + " of <X>")
	mve += rng + " is the " + lbl + " of <X>\n"
	final_lines.append(",".join(line))


fw = open('mve_output','w')
fw.write(mve)

fw2 = open('GS_with_mve.csv','w')
fw2.write("\n".join(final_lines))

