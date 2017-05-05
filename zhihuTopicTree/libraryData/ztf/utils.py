#coding=utf8
import json
import os


def get_son(url):
	import re

def main():
	layer=0
	for i in os.listdir('.'):
		rs=dict()
		rs['name']="中图法分类"
		rs['children']=[]
		if i.find('.txt')!=-1:
			with open(i) as f:
				rs=json.load(f)
				for j in rs['son']:
					print j
					cur=dict()
					if 'cat_id' in j and j['cat_id'].encode('utf8')!='图书分类号':
						name=j['cat_id'].encode('gbk')+':'+j['name'].encode('gbk')
						cur['name']=name]
						if 'href' in j:
							cur['children']=get_son(j['href'])
					rs['children'].append(cur)
				break

if __name__ == '__main__':
	main()
