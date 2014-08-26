#!/usr/bin/python
from datetime import date
import os.path, time
import os
import glob
import json

# global store
posts = list()

#######################
# dir: pdf_post/

pdf_post_dirs = './*.pdf'
files_full_path = glob.glob(pdf_post_dirs)
N = len(files_full_path)
for i in range(N):
	_date = date.fromtimestamp(os.path.getmtime(files_full_path[i])).strftime("%d %B %Y")
	name = os.path.basename(files_full_path[i])
	url = "/pdf_posts/" + name
	one_post = {'name':name, 'url':url, 'date':_date}
	posts.append(one_post)


#######################
#subidr in  pdf_post/
for root,folder,files in os.walk('./'):
	for x in folder:
		s = os.path.join(root,x)
		pdfs = glob.glob(s + '/*.pdf')
		for p in pdfs:
			_date = date.fromtimestamp(os.path.getmtime(p)).strftime("%d %B %Y")
			name = os.path.basename(p)
			url = "/pdf_posts/" + x + '/' + name
			one_post = {'name':name, 'url':url, 'date':_date}
			posts.append(one_post)

# echo
print 'Total num of pdf:',len(posts)

#write back
# open data file: pdf_posts.yml
json_file = open('../_data/pdf_posts.yml','w+')
json_file.write(json.dumps(posts,ensure_ascii = False, indent = 2, separators=(',',':')))
json_file.close()
