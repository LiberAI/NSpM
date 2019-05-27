import sys

"""
Section to parse the command line arguments.
"""

open_files = open(sys.argv[1],'r')
# Given format #
# ['Property', 'Label ', 'Range', 'Fuzzy Score', 'Comment about expr', 'URI', 'Number of Occurrences', 'MVE', 'Optimal Expression', 'SPARQL Query Template', 'Generator Query\r\n']

# Required format : separated by semi-colon ##
# [ class_name, empty, empty, NLQ (MVE), Sparql Query, Generator Query] #

lines = open_files.readlines()
open_files.close()
fl = 1

output = ""


"""
- 	We iterate over the lines of the document.
-	Convet the line into a list containig elements o the 
	string delimited by commas.
-	
"""
for line in lines:
	
	if fl:
		fl = 0
		continue
	l = line.split(',')
	
	# print l
	
	newl,to_remove = [],[]
	newl.append("dbo:Place")
	newl.append("")
	newl.append("")

	nlq = l[7].split()
	# The fuzzy score column is not present in the 
	# autmatically created csv file.
	""" if(len(l)==10):
		#print "Change"
		nlq = l[6].split()
 	"""
	"""
	From MVE column a question is selected and each word
	is put into as an element of the list.
	""" 
	for i in range(len(nlq)):
		if '(' in nlq[i] or ')' in nlq[i]:
			to_remove.append(nlq[i])
			continue
		if '<' not in nlq[i] and '?' not in nlq[i]:
			nlq[i] = nlq[i].lower()			

	for x in to_remove:
		nlq.remove(x)

	spq = l[-2].split()
	"""
	Query one
	"""
	for i in range(len(spq)):
		if '<' not in spq[i] and '?' not in spq[i]:
			spq[i] = spq[i].lower()
			
	"""
	Query two
	"""
	gq = l[-1].split()
	for i in range(len(gq)):
		if '<' not in gq[i] and '?' not in gq[i] and '[' not in gq[i]: 
			gq[i] = gq[i].lower()
			

	newl.append(" ".join(nlq))
	newl.append(" ".join(spq))
	newl.append(" ".join(gq))
	output += ";".join(newl) + "\n"


fw = open(sys.argv[2],'w')
fw.write(output)
fw.close()