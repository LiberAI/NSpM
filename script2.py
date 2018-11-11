f2 = open('data/temp.csv','rw')
f3 = open('data/newtemp.csv','w')

l2 = f2.readlines();

lines = f.readlines()
# print "xxxs"
cnt = 0
for line in l2:

	line = line.split(',')
	line.append("what is the " + line[0] + " of <X>")
	line.append("what is the " + line[0] + " of <X>")
	# print line
	# if line[1] == '':
	# 	line[1] = x[3].strip()
	# if line[2] == '':
	# 	line[2] = "what is the " + x[1] + " of <X>"
	# else:
	# 	line[2] = line[2].replace("x","<X>")
	# if line[3] == '':
	# 	line[3] = line[2]
	# else:
	# 	line[3] = line[3].replace("x","<X>")
	# print line
	# line[1]
	newline = ",".join(line)
	print newline
	f3.write(newline)
