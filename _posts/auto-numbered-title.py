#!/usr/bin/env python
import sys

section1 = "#"
section2 = "##"
section3 = "###"


l1 = 0;
l2 = 0;
l3 = 0;

def IsSourceCode(line_0,i):
    is_source_code = 0
    if line_0.startswith("{% highlight") or line_0.startswith("{% endhighlight"):
        print "got one in line:",i
        is_source_code = 1
    
    return is_source_code


def IsHeader(line_0,line_1):
    global section1,section2,section3
    result = 0
    if line_0.startswith(section1) and not line_0.startswith(section2):
        result = 1
    elif line_1.startswith("==="): 
        result = 11
    elif line_0.startswith(section2) and not line_0.startswith(section3):
        result = 2
    elif line_1.startswith("----"): 
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

    now_in_code_block = False

    for i in range(6,len(_all_lines)-1):
        line = _all_lines[i]

        #is code block?
        code_flag = IsSourceCode(_all_lines[i],i)
        if code_flag == 1:
            now_in_code_block = not now_in_code_block
        if now_in_code_block == True:
            print "continue in line:",i
            continue

        Head = IsHeader(_all_lines[i],_all_lines[i+1])
        if 0 == Head:
            continue
        if 1 == Head:
            l1 = l1 + 1
            _number = str(l1)
            _all_lines[i] = line[0:1] + _number + " " +  line[1:]

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
            _all_lines[i] = line[0:2] + _number + " " +  line[2:]

            l3 = 0
        if 22 == Head:
            l2 = l2 + 1
            _number = str(l1 )+ "." + str(l2)
            _all_lines[i] = _number + " " +  line[:]

            l3 = 0
        if 3 == Head:
            l3 = l3 + 1
            _number = str(l1)+ "." + str(l2)+ "." + str(l3)
            _all_lines[i] = line[0:3] + _number + " " +  line[3:]

    _post = open(filename,'w+')
    _post.write("".join(_all_lines))
    _post.close()


if __name__=="__main__":
    filename = sys.argv[1]
    if None == filename:
        print "file name is None!"
        sys.exit(0) 
    AutoNumber(filename)
