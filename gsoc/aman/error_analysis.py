import sys

f = open(sys.argv[1],'r')
g = open(sys.argv[2],'r')


fl = f.readlines()
gl = g.readlines()
tot = 0
entity_error, prop_error = 0, 0

for i in range(len(fl)):
	if fl[i].strip() == gl[i].strip():
		# print fl[i], gl[i]
		continue
	myout = fl[i].strip().split()
	myEntity, myProp = "", ""
	for t in myout:
		if 'dbr_' in t:
			myEntity = t
		if '<' in t:
			myProp = t[1:-1]			

	reqout = gl[i].strip().split()
	reqEntity, reqProp = "", ""
	for t in reqout:
		if 'dbr_' in t:
			reqEntity = t
		if '<' in t:
			reqProp = t[1:-1]			

	if reqEntity != myEntity:

		# print myEntity, reqEntity
		entity_error += 1
	if reqProp != myProp:
		print reqProp, myProp
		prop_error += 1
	tot += 1	

print (99/2034.0)
