import sys 

f = open(sys.argv[1],'rw')
lines = f.readlines()

to_del = [3636, 15366, 22096, 23913, 27938, 29413, 29452, 33507, 34670, 50813, 58739, 71547, 71747, 72127, 72699, 73110, 73146, 75803, 76512, 76977]
to_del.reverse()

for x in to_del:
	del lines[x-1]

lines = "".join(lines)
print lines