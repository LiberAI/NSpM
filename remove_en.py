import sys

f = open(sys.argv[1],'rw')
lines = f.readlines()

final = []
lineno = []
i = 0
for l in lines:
	i += 1
	if ' en ' in l:
		lineno.append(i)

# print "\n".join(lineno)
print lineno