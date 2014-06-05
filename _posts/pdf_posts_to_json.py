#!/usr/bin/python
from datetime import date
import os.path, time
import os
import glob
import json

pdf_post_dirs = '../pdf_posts/*.pdf'


#print glob.glob(pdf_post_dirs)
files_full_path = glob.glob(pdf_post_dirs)

N = len(files_full_path)
print N
posts = list()
for i in range(N):
	_date = date.fromtimestamp(os.path.getmtime(files_full_path[i])).strftime("%d %B %Y")
	name = os.path.basename(files_full_path[i])
	url = "/pdf_posts/" + name
	one_post = {'name':name, 'url':url, 'date':_date}
	posts.append(one_post)

#echo test
#for post in posts:
#	print post['date']
#	print post['name']
#	print post['url']
	
#write back
# open data file: pdf_posts.yml
json_file = open('../_data/pdf_posts.yml','w+')
json_file.write(json.dumps(posts,ensure_ascii = False, indent = 2, separators=(',',':')))
json_file.close()
