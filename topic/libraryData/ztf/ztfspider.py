#coding=utf8
import requests
import lxml.html,json,re


def dps():
	start_url='http://ztflh.xhma.com'
	layer=0
	id='1'
	next_url=[{'url':start_url,'id':id}]
	while  True:
		tmp=[]
		if len(next_url)==0:
			break
		for i in next_url:
			url=i['url']
			cur_id=i['id']
			tmp.extend(parse_html(url,cur_id,layer))
		layer+=1
		print str(layer)+':'+str(len(tmp))
		next_url=tmp
	
def parse_html(url,cur_id,layer):
	content=requests.get(url).content
	data={'id':cur_id}
	son=[]
	son_url=[]
	etree=lxml.html.fromstring(content)
	cat_xpath='//div[@class="data"]//li'
	etree=etree.xpath(cat_xpath)
	for i in etree:
		rs=dict()
		cat_xpath2='./span/text()'
		tmp=i.xpath(cat_xpath2)
		if len(tmp)>0:
			rs['cat_id']=''.join(tmp)
			tmp2=i.xpath('./a/@href')
			if len(tmp2)>0:
				rs['href']=''.join(tmp2)
				rs['name']=''.join(i.xpath('./a/text()'))
				id=re.search('[0-9]+',rs['href'])
				if id:
					son_url.append({'url':rs['href'],'id':id.group()})
			else:
				rs['name']=''.join(i.xpath('./text()'))
		son.append(rs)
	data['son']=son
	with open('layer'+str(layer)+'_'+str(cur_id)+'.txt', 'w') as f:
		f.write(json.dumps(data))
	return son_url

if __name__ == '__main__':
	dps()
