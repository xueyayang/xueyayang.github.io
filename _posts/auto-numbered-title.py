#!/usr/bin/env python
import sys

section1 = "#"
section2 = "##"
section3 = "###"


l1 = 0;
l2 = 0;
l3 = 0;


def IsHeader(line_0,line_1):
    global section1,section2,section3
    result = 0
    if line_0.startswith(section1) and not line_0.startswith(section2):
        result = 1
    elif line_1.startswith("==="): 
        result = 11
    elif line_0.startswith(section2) and not line_0.startswith(section3):
        result = 2
    elif line_1.startswith("------"): 
        result = 22
    elif line_0.startswith(section3):
        result = 3
    else:
        result = 0
        
    return result




def AutoNumber(filename):
    global section1,section2,section3,l1,l2,l3
    _post = open(filename,'r');
    _all_lines = _post.readlines(); 
    _post.close();

    for i in range(6,len(_all_lines)-1):
        line = _all_lines[i]
        Head = IsHeader(_all_lines[i],_all_lines[i+1])
        if 0 == Head:
            continue
        if 1 == Head:
            l1 = l1 + 1
            _number = str(l1)
            _all_lines[i] = line[0:2] + _number + " " +  line[2:]

            l2 = 0
            l3 = 0
        if 11 == Head:
            l1 = l1 + 1
            _number = str(l1)
            _all_lines[i] = _number + " " +  line[:]

            l2 = 0
            l3 = 0
        if 2 == Head:
            l2 = l2 + 1
            _number = str(l1 )+ "." + str(l2)
            _all_lines[i] = line[0:3] + _number + " " +  line[3:]

            l3 = 0
        if 22 == Head:
            l2 = l2 + 1
            _number = str(l1 )+ "." + str(l2)
            _all_lines[i] = _number + " " +  line[:]

            l3 = 0
        if 3 == Head:
            l3 = l3 + 1
            _number = str(l1)+ "." + str(l2)+ "." + str(l3)
            _all_lines[i] = line[0:4] + _number + " " +  line[4:]


    _post = open(filename,'w+')
    _post.write("".join(_all_lines))
    _post.close()


if __name__=="__main__":
    filename = sys.argv[1]
    if None == filename:
        print "file name is None!"
        sys.exit(0) 
    AutoNumber(filename)
