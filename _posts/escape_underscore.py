#!/usr/bin/env python
import sys

now_in_code_block = False

def open_code_block():
	global now_in_code_block
	now_in_code_block = True

def close_code_block():
	global now_in_code_block
	now_in_code_block = False


def Escape_Underscore(filename):
	_post = open(filename,'r')
	_all_lines = _post.readlines();
	_post.close();


	for i in  range(0,len(_all_lines)):
		line = _all_lines[i]

		if line.startswith("{% highlight"):
			open_code_block()
		elif line.startswith("{% endhighlight"):
			close_code_block()
		elif now_in_code_block == True: #skip code block
			print "skip source line:", i + 1
			continue
		elif line.startswith("["):#skip reference line
			print "skip reference line:", i + 1
			continue
		else:
			temp = line.replace("_","\_")

			if temp != line:
				print "replace line:", i + 1
				print "from:"
				print "\t", line
				print "to:"
				print "\t", temp
				_all_lines[i] = temp #write to _all_lines[i]

	#write back
	_post = open(filename, 'w+')
	_post.write("".join(_all_lines))
	_post.close()

			

def Test_Replace():
	print 'this_is_test'.replace('_',' ')

if __name__=="__main__":
	filename = sys.argv[1]
	if None == filename:
		print "file name is None!"
		sys.exit(0)
	Escape_Underscore(filename);
	#Test_Replace()
