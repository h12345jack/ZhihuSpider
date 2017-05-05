#coding=utf8

import lxml.html

# def main():
# 	with open('lcc.html') as f:
# 		content=f.read()
# 		etree=lxml.html.fromstring(content)
# 		c1_xpath='//h3/span[@class="mw-headline"]/text()'
# 		c2_xpath='//ul'
# 		c1=etree.xpath(c1_xpath)
# 		c2=etree.xpath(c2_xpath)
# 		print len(c1)
# 		print len(c2)
# 		for i,j in zip(c1,c2):
# 			c2=j.xpath('.//li')
# 			print i.encode('utf8')
# 			print ','.join([''.join([j.encode('utf8') for j in i.xpath('./text()')]) for i in c2])
# 			print len(c2)
# 			print '*'*10
# def main():
# 	f2=open('lcc_3.txt','w')
# 	early=''
# 	with open('lcc_2.txt') as f:
# 		for i in f.readlines():
# 			i=i.strip()
# 			num=i.count('~')
# 			if num!=0 or i.find('CLASS')!=-1 or i.find('Subclass')!=-1:
# 				f2.write(early+'\n')
# 				early=i
# 			else:
# 				early+=i
# 	f2.write(early+'\n')

# def main():
# 	
# 	with open('lcc_2.txt') as f:
# 		x=1
# 		for i in f.readlines():
# 			if i.find('CLASS')!=-1:
# 				rs[0].append(i)
# 				continue
# 			if i.find('Subclass')!=-1:
# 				rs[1].append(i)
# 				continue
# 			num=i.count('~')
# 			if num!=0:
# 				early=i
# 			else:
# 				i=early
# 			early=i
# 			if i.count('~')==0:print i
# 			print i.count('~')

def _get_the_layer(i):
	if i.find('CLASS')!=-1:
		return 1
	elif i.find('Subclass')!=-1:
		return 2
	else:
		num=i.count('~')
		return num+2

def _pop_it(rs_stack,layer):
	if len(rs_stack[layer+1])==0:
		tmp=rs_stack[layer]
		rs_stack[layer]=[]
		return tmp
	else:
		rs_stack[layer][-1]['children']=_pop_it(rs_stack,layer+1)
		tmp=rs_stack[layer]
		rs_stack[layer]=[]
		return tmp
def modify_i(i):
	return i[:i.find('~')]

def _push_it(rs_stack,i,layer):
	rs=dict()
	if len(rs_stack[layer])==0 or len(rs_stack[layer+1])==0:
		rs['name']=modify_i(i)
		rs['children']=[]
		rs_stack[layer].append(rs)
	else:
		rs_stack[layer][-1]['children']=_pop_it(rs_stack,layer+1)
		rs['name']=modify_i(i)
		rs['children']=[]
		rs_stack[layer].append(rs)
		

	

def main():
	rs_stack=[[] for i in range(15)]
	rs=dict()
	rs['name']='root'
	rs['children']=[]
	rs_stack[0].append(rs)
	with open('lcc_3.txt') as f:
		for i in f.readlines():
			i=i.strip()
			layer=_get_the_layer(i)
			_push_it(rs_stack,i,layer)
		_push_it(rs_stack,'root',0)
	import json
	f=file('lcc2.rs','w')
	f.write(json.dumps(rs_stack[0][0]))


if __name__ == '__main__':
	main()