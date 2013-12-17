#!/usr/bin/env python

section1 = "##"
section2 = "###"
section3 = "####"


l1 = 0;
l2 = 0;
l3 = 0;

filename = 'A20.md'

_post = open(filename,'r');
_all_lines = _post.readlines(); 
_post.close();

for i in range(0,len(_all_lines)):
	line = _all_lines[i]
	if line.startswith(section1) and not line.startswith(section2):
		l1 = l1 + 1
		_number = str(l1)
		_all_lines[i] = line[0:1] + _number + " " +  line[2:]

		l2 = 0
		l3 = 0
	if line.startswith(section2) and not line.startswith(section3):
		l2 = l2 + 1
		_number = str(l1 )+ "." + str(l2)
		_all_lines[i] = line[0:2] + _number + " " +  line[3:]

		l3 = 0
	if line.startswith(section3):
		l3 = l3 + 1
		_number = str(l1)+ "." + str(l2)+ "." + str(l3)
		_all_lines[i] = line[0:3] + _number + " " +  line[4:]


_post = open(filename,'w+')
_post.write("".join(_all_lines))
_post.close()
