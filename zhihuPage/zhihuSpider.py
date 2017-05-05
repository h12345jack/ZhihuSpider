#coding=utf8

"""抓取知乎话题结构的爬虫
使用多线程优化
"""

import os
import re
import json
import time

import requests
import lxml
import lxml.html
from lxml import etree


from config.Config import URL
from config.Config import DATA_DIR
from config.Config import HEADERS,TIMEOUT
from config.Config import COOKIES_RAW_PATH,COOKIES_PATH,XSRF_PATH
from config.Config import TOPIC_ID_LIST


CUR_DIR = os.path.dirname(os.path.abspath('.'))
DEBUG = False
NOW = time.strftime("%Y-%m-%d", time.localtime())
TIME_SLEEP = 2
RETRY = 5

ERROR_DIR = os.path.join(CUR_DIR,'error')
if not os.path.exists(ERROR_DIR):
    os.mkdir(ERROR_DIR)

class ZhihuSpider(object):
    """抓取知乎Topic的爬虫,返回一个spider的句柄，执行常规的post，get即可"""
    def __init__(self):
        self.dir_root = CUR_DIR

        self.url_homepage = URL['HOMEPAGE']
        self.headers_base = HEADERS

        self.url_login = URL['LOGIN']
        self.url_prefix = URL['QUESTION_PREFIX']
        self.url_questions = URL['QUESTIONS']

        self.timeout_query = TIMEOUT

        self.spider = requests.Session()
        self.spider.headers = self.headers_base
        self.spider.timeout = None

    def _get_xsrf(self, url=None):
        try:
            res = self.spider.get(url,
                                  headers=self.headers_base,
                                  timeout=self.timeout_query)
        except Exception as e:
            logging.debug('Failed to fetch {0}. Error: {1}'.format(url, e))
            sys.exit(-1)

        try:
            html_con = etree.HTML(res.text)
        except Exception as e:
            logging.debug('Fail to form dom tree. Error: {1}'.format(url, e))
            sys.exit(-1)

        node_xsrf = html_con.xpath("//input[@name='_xsrf']")[0]

        xsrf = node_xsrf.xpath("@value")[0]

        logging.debug('xsrf for {0}: {1}'.format(url, xsrf))

        return xsrf

    def login_method1(self):
        xsrf = self._get_xsrf(url=self.url_homepage)
        self.payload_login['_xsrf'] = xsrf
        with open(_XSRF_GLOBAL_FIELNAME,'w') as f:
            f.write(xsrf)
        try:
            self.spider.post(self.url_login,
                             headers=self.headers_base,
                             data=self.payload_login,
                             timeout=self.timeout_query)
        except Exception as e:
            logging.debug('Failed to try to login. Error: {0}'.format(e))
        return self._test_login()

    def login_method2(self):
        self.clean_cookies2cookies_data()
        with open(COOKIES_PATH) as f:
            cookies=json.loads(f.read())
            requests.utils.add_dict_to_cookiejar(self.spider.cookies, cookies)
            with open(XSRF_PATH,'w') as f:
                f.write(cookies['_xsrf'])
        return self._test_login()

    def login(self):
        """登陆
        """
        if self.login_method2():
            print u'登录2',
            print 'Login successfully! '
            return self.spider
        else:
            print 'Failed!'
            sys.exit(-1)


    
    def clean_cookies2cookies_data(self):
        """make cookies raw to a json
        """
        with open(COOKIES_RAW_PATH) as f:
            line=f.readline()
            line=line.split(';')
            cookies=dict()
            for i in line:
                index=i.find('=')
                value=i[index+1:].strip()
                value=value.replace('"','')
                cookies[i[:index].strip()]=value
            rs_f=file(COOKIES_PATH,'w')
            rs_f.write(json.dumps(cookies))

    def _test_login(self):
        """测试是否登陆成功.

        Output:
        + 测试成功时返回 True，否则返回 False.
        """
        try:
            res = self.spider.get(self.url_homepage,
                                  headers=self.headers_base,
                                  timeout=self.timeout_query)
        except Exception as e:
            print res.content
            logging.debug('Error when testing login: {0}'.format(e))
            return False

        try:
            html_con = etree.HTML(res.text)
        except Exception as e:
            logging('Failed to set dom tree: {0}'.format(e))
            return False

        # print res.content

        node_list_title = html_con.xpath("//div[@id='zh-home-list-title']")

        if node_list_title:
            return True
        else:
            return False

    def run(self):
        """总控
        """
        self.login()
        self.crawl_by_layer()

def spider_get(spider,url,retry):

    if retry > 0:
        try:
            res = spider.get(url,headers = HEADERS)
            content = res.content
        except(requests.packages.urllib3.exceptions.ProtocolError,
              requests.exceptions.ConnectionError):
            if retry -1 >0:
                print('ConnectionError: 断开连接!进行重试,还剩' + str(
                            retry - 1) + '次重试机会')
            elif retry - 1 == 0:
                print('ConnectionError: 断开连接!进行最后一次重试')
            time.sleep(5)

            return spider_get(spider,url,retry - 1)
        else:
            return content
    else:
        print(url)
        print('最后一次重试失败!放弃尝试重新连接!')



def topic2question(spider,url):
    topic_id=re.search('[0-9]+',url).group()
    rs_f = file(os.path.join(DATA_DIR,topic_id+'.txt'),'w')
    cur_page=0
    next_url=url

    for tmp in range(51):
        time.sleep(TIME_SLEEP)

        content=spider_get(spider,next_url,retry= RETRY)

        etree=lxml.html.fromstring(content)
        link_xpath='//a[@class="question_link"]/@href'
        link=etree.xpath(link_xpath)
        link2=set(link)
        for i in link2:
            rs_f.write("http://zhihu.com"+i+'\n')
        #next page
        next_page_link_xpath='//div[@class="zm-invite-pager"]/span/a/@href'
        next_page_link=etree.xpath(next_page_link_xpath)
        if len(next_page_link)==0:
            with open(os.path.join(ERROR_DIR,topic_id+'_'+str(cur_page)+".txt"),'w') as f:
                f.write(content)
                break
        last_page=next_page_link[-1]
        tmp=re.search('[0-9]+',last_page)
        if tmp:
            last_page=tmp.group()
        else:
            break
        print topic_id,cur_page,last_page
        if cur_page<int(last_page):
            cur_page=int(last_page)
            next_url=url+'?page='+last_page
        else:
            break


def topic_list_spider():
    zhihu_spider = ZhihuSpider()
    spider = zhihu_spider.login()
    for i in TOPIC_ID_LIST:
        url = 'https://www.zhihu.com/topic/{}/top-answers'.format(i)
        topic2question(spider,url)
        
def test():
    zhihu_spider = ZhihuSpider()
    spider = zhihu_spider.login()
    url = 'https://www.zhihu.com/topic/19551771/top-answers'
    topic2question(spider,url)

if __name__ == '__main__':
    topic_list_spider()
    # zhihu_spider = ZhihuSpider()
    # zhihu_spider.run()
