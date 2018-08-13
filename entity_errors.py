import sys

f = open(sys.argv[1],'r')
g = open(sys.argv[2],'r')
h = open(sys.argv[3],'r')


fl = f.readlines()
gl = g.readlines()
hl = h.readlines()
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
save = []
for i in range(len(gl)):
	testout = gl[i].strip().split()
	testEntity = ""
	for t in testout:
		if 'dbr_' in t:
			testEntity = t
			if testEntity[1:-1] in train_entities:
				save.append(i);
				cnt += 1
	tot += 1

newtest_nlq, newtest_sparql = [], []

for i in save:
	newtest_sparql.append(gl[i])

for i in save:
	newtest_nlq.append(hl[i])

# print "".join(newtest_sparql)
print "".join(newtest_nlq)


# print cnt, tot


