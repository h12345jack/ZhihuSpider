# -*- coding:utf-8 -*-

import sys
import os
import random
import time
import json
import re
from urllib import urlencode
from datetime import datetime
import logging


import lxml.html as ET
import requests

from scrapy.selector import Selector
from scrapy.spiders import Spider
from scrapy.http import Request

from zhihuSpider.util import getTasks,time_sleep_random
from zhihuSpider.items import ZhihuQuestionItem, ZhihuAnswerItem, ZhihuQuestionLogItem
from zhihuSpider.settings import HEADER,DATA_STORE_DIR,INCLUDE
from zhihuSpider.zhihu_spider import zhihu_spider

DELAY_M= 0.5
RETRY = 5
HOST='http://www.zhihu.com'



def spider_get(spider,url,retry):

    if retry > 0:
        try:
            res = spider.get(url,headers = HEADER)
            content = res.content
        except(requests.packages.urllib3.exceptions.ProtocolError,
              requests.exceptions.ConnectionError):
            if retry -1 >0:
                print u'ConnectionError: 断开连接!进行重试,还剩' + str(
                            retry - 1) + u'次重试机会'
            elif retry - 1 == 0:
                print u'ConnectionError: 断开连接!进行最后一次重试'
            time.sleep(1.0)

            return spider_get(spider,url,retry - 1)
        else:
            return content
    else:
        logging.warning(url,' retry too many times')
        print u'最后一次重试失败!放弃尝试重新连接!'

def spider_post(spider, url ,data, retry):
    if retry > 0:
        try:
            res = spider.post(url,data=data, headers = HEADER)
            content = res.content
        except(requests.packages.urllib3.exceptions.ProtocolError,
              requests.exceptions.ConnectionError):
            if retry -1 >0:
                print u'ConnectionError: 断开连接!进行重试,还剩' + str(
                            retry - 1) + u'次重试机会'
            elif retry - 1 == 0:
                print u'ConnectionError: 断开连接!进行最后一次重试'
            time.sleep(1.0)

            return spider_get(spider,url,retry - 1)
        else:
            return content
    else:
        logging.error(url,' retry too many times')
        print u'最后一次重试失败!放弃尝试重新连接!'

def retry(attemp):
    def decorator(func):
        def wrapper(*args, **kw):
            att = 0
            while att<attempt:
                try:
                    return func(*args,**kw)
                except Exception as e:
                    att+=1
        return wrapper
    return decorator



class ZhihuSpider(Spider):
    name = 'zhihu_question'
    allowed_domains = ['zhihu.com']
    start_urls = []

    def __init__(self, filename=None, *a,  **kwargs):
        self.user_names = []
        self.data_dir=DATA_STORE_DIR
        self.start_urls = getTasks()
        zp=zhihu_spider()
        self.spider = zp.login()
        self._xsrf2 = zp._xsrf
        self.spider.keep_alive=False
        
    def start_requests(self):
        '''开始整个爬虫，登陆'''
        for url in self.start_urls:
            yield Request(url, callback = self.parse_question)
            print url,'to crawl'

    def parse_question(self,response):
        '''抓取问题'''
        url = response.url
        q_id = "".join(re.findall(r'question/([0-9]+)',url))

        html_content = response.body
        file_path = os.path.join(self.data_dir,q_id+'.html')
        with open(file_path,'w') as f:
            print>>f,html_content
        
        data_xpath = '//*[@id="data"]/@data-state'
        et = ET.fromstring(html_content)
        data = et.xpath(data_xpath)
        q_data = [json.loads(d) for d in data]
        

        zhihu_q = ZhihuQuestionItem()

        zhihu_q["q_id"] = q_id
        zhihu_q["q_url"] = url
        zhihu_q["q_data"] = q_data

        zhihu_q['q_answer_list'] = self.getAnswerList(q_id)
        zhihu_q['q_log_list'] = self.parse_log(url)
        print q_id,"yield to pipline"
        yield zhihu_q

    def getAnswerList(self,q_id):
        '''抓取答案'''
        offset = 0
        total = 0
        req = requests.Session()
        data_list = []
        while offset <= total:
            time_sleep_random(DELAY_M, DELAY_M*2)
            data = {
                "include":INCLUDE,
                "offset": offset,
                "limit": 20,
                "sort_by": "default"
            }
            url = "https://www.zhihu.com/api/v4/questions/{}/answers".format(q_id)
            res = req.get(url, params = data, headers = HEADER)
            html_content = res.content
            json_data = json.loads(html_content)
            data_list.append(json_data)
            total = int(json_data["paging"]["totals"])
            file_path = os.path.join(self.data_dir,q_id+'-'+str(offset)+'-'+str(offset+20)+'.json')
            with open(file_path,'w') as f:
                print>>f,html_content
            offset += 20
        zhihu_a = ZhihuAnswerItem()
        zhihu_a['a_data'] = data_list
        return zhihu_a

    def parse_log_item(self,html_content):
        '''解析那些item'''
        log_list=[]
        html=ET.fromstring(html_content)
        item_xpath='//*[@class="zm-item"]'
        item=html.xpath(item_xpath)
        somebody_xpath = ".//a[@data-tip][1]/@href"
        do_xpath = './/span[@class="zg-gray-normal"]'
        something_xpath = './/text()'
        action_id_xpath = './/div[@class="zm-item-meta"]/text()'
        sometime_xpath = ".//*[@datetime]/@datetime"
        def clean_hh(content):
            content=content.replace('\n\n','')
            return content
        for i in item:
            tmp=ZhihuQuestionLogItem()
            tmp['action_something']=clean_hh(''.join(i.xpath(something_xpath)))
            tmp['action_somebody']="".join(i.xpath(somebody_xpath))
            tmp['action_do']=''.join([j.text_content() for j in i.xpath(do_xpath)])
            tmp['action_id']=clean_hh(''.join(i.xpath(action_id_xpath))).replace('\n','')
            tmp['action_time']=''.join(i.xpath(sometime_xpath))
            log_list.append(tmp)
        return log_list

    def parse_log(self,url):
        '''从url开始获取log信息'''
        q_id_tmp=re.findall('[0-9]+',url)
        if len(q_id_tmp)==0:return []
        q_id=''.join(q_id_tmp)
        log_url='https://www.zhihu.com/question/'+q_id+'/log'
        html_content=spider_get(self.spider, url= log_url, retry= RETRY)

        print log_url

        log_list=self.parse_log_item(html_content)
        item_id_xpath='//*[@class="zm-item"]/@id'
        last_item_id=ET.fromstring(html_content).xpath(item_id_xpath)[-1]
        for iters in range(50):
            print log_url, "sleep",DELAY_M
            time.sleep(DELAY_M*0.2)
            tmp=re.findall(r'[0-9]+',last_item_id)
            last_item_id=''.join(tmp)
            data={'start':last_item_id,
                  'offset':20,
                  '_xsrf': self._xsrf2}
            rs=spider_post(self.spider, url=log_url, data=data, retry= RETRY)
            json_data=json.loads(rs)
            msg=json_data['msg']

            if msg[0]>0:
                content=msg[1]
                another_list=self.parse_log_item(content)
                last_item_id=ET.fromstring(content).xpath(item_id_xpath)[-1]
                log_list.extend(another_list)
            else:
                break
        return log_list


  