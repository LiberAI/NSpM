import sys

f = open(sys.argv[1],'r')
g = open(sys.argv[2],'r')


fl = f.readlines()
gl = g.readlines()
tot = 0
entity_error, prop_error = 0, 0
train_entities = set()

for i in range(len(fl)):
	trainout = fl[i].strip().split()
	for t in trainout:
		if 'dbr_' in t:
			train_entities.add(t[1:-1]);
			break

# print train_entities

cnt = 0
for i in range(len(gl)):
	testout = gl[i].strip().split()
	testEntity = ""
	for t in testout:
		if 'dbr_' in t:
			testEntity = t
			print testEntity
			if testEntity in train_entities:
				cnt += 1
	tot += 1


print cnt, tot


