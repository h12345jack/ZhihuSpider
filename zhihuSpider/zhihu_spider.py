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


from zhihuSpider.config.Config import URL
from zhihuSpider.config.Config import DATA_DIR
from zhihuSpider.config.Config import HEADERS,TIMEOUT
from zhihuSpider.config.Config import COOKIES_RAW_PATH,COOKIES_PATH,XSRF_PATH


CUR_DIR = os.path.dirname(os.path.abspath('.'))
DEBUG = False
NOW = time.strftime("%Y-%m-%d", time.localtime())
TIME_SLEEP = 2
RETRY = 5

ERROR_DIR = os.path.join(CUR_DIR,"zhihuSpider",'error')
if not os.path.exists(ERROR_DIR):
    os.mkdir(ERROR_DIR)

class zhihu_spider(object):
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
            self._xsrf = cookies['_xsrf']
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


if __name__ == '__main__':
    zhihu_spider = ZhihuSpider()
    zhihu_spider.run()
