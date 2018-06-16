f = open('manual.csv','rw')
f2 = open('temp.csv','rw')
f3 = open('newtemp.csv','w')

l2 = f2.readlines();

lines = f.readlines()
# print "xxxs"
cnt = 0
for line in lines:
	if cnt <= 200:
		cnt += 1
		continue
	line = line.split(',')
	x = l2[cnt-1].split(',')
	# print line
	if line[1] == '':
		line[1] = x[3].strip()
	if line[2] == '':
		line[2] = "what is the " + x[1] + " of <X>"
	else:
		line[2] = line[2].replace("x","<X>")
	if line[3] == '':
		line[3] = line[2]
	else:
		line[3] = line[3].replace("x","<X>")
	# print line
	# line[1]
	newline = ",".join(line)
	print newline
	f3.write(newline)
	# print
	cnt += 1
	# if cnt > 200:
	# 	break