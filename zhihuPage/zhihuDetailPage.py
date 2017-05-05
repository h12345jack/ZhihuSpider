#coding=utf8

import logging
import ConfigParser
import time
import json
import re
import HTMLParser


import requests
import lxml.html as html
from lxml.html import clean

from config.Config import HEADERS,RECOMMENDATIONS_URL,INCLUDE



def getQuestion(url):
    q_id = "".join(re.findall(r'question/([0-9]+)',url))
    req = requests.Session()
    req.headers.update(HEADERS)
    res = req.get(url)
    html_content = res.content
    with open(q_id+'.html','w') as f:
        print>>f,html_content

def getAnswerList(q_id):
    offset = 0
    total = 0
    while offset <= total:
        time.sleep(0.5)
        data = {
            "include":INCLUDE,
            "offset": offset,
            "limit": 20,
            "sort_by": "default"
        }
        url = "https://www.zhihu.com/api/v4/questions/{}/answers".format(q_id)
        req = requests.Session()
        res = req.get(url, params = data, headers = HEADERS)
        html_content = res.content
        json_data = json.loads(html_content)
        print json_data
        total = int(json_data["paging"]["totals"])
        with open(q_id+'-'+str(offset)+'-'+str(offset+20)+'.json','w') as f:
            print>>f,html_content
        offset += 20
        print res.url

def topic_parse():
    with open('57868057.html') as f:
        content = f.read()
        et = html.fromstring(content)
        title_xpath = '//h1'
        topic_tag_xpath = '//*[@data-za-module="TopicItem"]'
        desc_xpath = '//*[@class="QuestionHeader-detail"]'
        followee_num_xpath = '//*[@class="NumberBoard QuestionFollowStatus-counts"]'
        h = HTMLParser.HTMLParser()
        cleaner = clean.Cleaner(scripts=True,
                                    javascript=True,
                                    comments=True,
                                    safe_attrs=[])
        def element_print(ele):
            return h.unescape(html.tostring(cleaner.clean_html(ele)))

        print ",".join([element_print(i) for i in et.xpath(title_xpath)])
        print ",".join([element_print(i) for i in et.xpath(topic_tag_xpath)])
        print ",".join([element_print(i) for i in et.xpath(desc_xpath)])
        print ",".join([element_print(i) for i in et.xpath(followee_num_xpath)])
        data_xpath = '//*[@id="data"]/@data-state'
        data_state = json.loads(et.xpath(data_xpath)[0])
        f = file('57868057_q.json','w')
        print>>f, json.dumps(data_state)

# def getRecommendations():
#     '''解析获取推荐信息？？'''
#     with open('57868057.html') as f:
#         html_content = f.read()
#         udid = "".join(re.findall(r'xUDID&quot;\:&quot;(\S+?)&quot;',html_content))
#         new_header = HEADERS
#         new_header['x-udid'] = udid

#         recommendations = req.get(RECOMMENDATIONS_URL,headers = new_header)
#         with open(q_id + '_recommendations.json','w') as f:
#             print>>f,recommendations.content



def test():
    url = 'https://www.zhihu.com/question/57868057'
    getQuestion(url)
    getAnswerList('57868057')
    # getUid()
    # topic_parse()

def main():
    topic_parse()  

if __name__ == '__main__':
    main()
