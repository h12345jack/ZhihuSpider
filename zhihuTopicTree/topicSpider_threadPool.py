#coding=utf8

"""抓取知乎话题结构的爬虫
使用多线程优化
"""

import os
import sys
import json
import time
import logging
import threading
from multiprocessing.dummy import Pool as ThreadPool

import requests
import lxml
import copy 
from lxml import etree
from lxml.html import document_fromstring

from utils import get_configs

lock1 = threading.Lock()

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=time.strftime("%Y-%m-%d", time.localtime())+'_cralwer.log',
                filemode='w')

urllib3_logger = logging.getLogger('requests')
urllib3_logger.setLevel(logging.WARNING)


CUR_DIR = os.path.dirname(os.path.abspath(__file__))
CUR_FNAME_SETTINGS = os.path.join(CUR_DIR, 'data','settings.yaml')
CUR_CONFIGS = get_configs(CUR_FNAME_SETTINGS)
CUR_HEADERS_BASE = CUR_CONFIGS['HEADERS']['BASE']
CUR_TIMEOUT_QUERY = CUR_CONFIGS['TIMEOUT']['QUERY']
COOKIES=os.path.join(CUR_DIR,'data','cookies.data')
COOKIES_RAW=os.path.join(CUR_DIR,'data','cookies_raw.data')
_XSRF_GLOBAL_FIELNAME =  os.path.join(CUR_DIR,'data','_xsrf.dat')

DEBUG = False

NOW = time.strftime("%Y-%m-%d", time.localtime())


def multi_run_wrapper(args):
    spider=args[0]
    id=args[1]
    topic_f=args[2]
    topic_log_f = args[3]
    return get_topics(spider,id,topic_f,topic_log_f)


def get_topics(spider,id,topic_f,topic_log_f):
    '''
    spider为requests对象，
    id为话题id
    topic_f为layer*.json句柄
    topic_log_f为xxxx-xx-xx_crawler.log句柄
    '''
    url='https://www.zhihu.com/topic/'+id+'/organize/entire'
    time.sleep(0.1)
    for counter1 in range(1000):
        try:
            res = spider.get(url,headers=CUR_HEADERS_BASE,
                            timeout=CUR_TIMEOUT_QUERY)

            content=res.content
            etree=lxml.html.fromstring(content)

            people_xpath='//div[@class="zm-topic-side-followers-info"]//strong/text()'
            des_xpath='//div[@id="zh-topic-desc"]'
            name_xpath='//h1/text()'
            etree_id=etree.xpath(people_xpath)
            etree_des=etree.xpath(des_xpath)
            etree_name=etree.xpath(name_xpath)

            topic=dict()
            topic['id']=id
            topic['followers']=etree_id[0] if len(etree_id)>0 else 0
            topic['des']=lxml.html.tostring(etree_des[0],encoding='utf8') if  len(etree_id)>0 else 'NULL'
            topic['name']=etree_name[0]
            
            with open(_XSRF_GLOBAL_FIELNAME) as f:
                _xsrf=f.read()

            data_xsrf={'_xsrf':_xsrf}

        except BaseException , e:
            if str(e)!='None':
                logging.debug('Fail to fetch the page. Error: {0}.'.format(e))
            logging.debug(url+' wait for a sec to recrawl')
            if counter1>500:logging.warning(url+' fail more than 500')
            time.sleep(1)
        else:
            if counter1>10:print url,'more 10 tries, get data get!'
            break
    
    url2=url
    son_by_json=set()

    for tmp in range(2000):
        
        time.sleep(0.1)

        def post_func(url):
            res2=spider.post(url, data=data_xsrf,
                             headers=CUR_HEADERS_BASE,
                             timeout=CUR_TIMEOUT_QUERY)
            data=json.loads(res2.content)
            return data

        for counter in range(1000):
            try:
                data = post_func(url2)
            except BaseException as e:
                if str(e)!='None': print e
                if counter>50:print url2,'retry',counter+1
                time.sleep(0.5)
            else:
                if counter>10:print url2,'more 10 tries, post data get!'
                break

        msg=data['msg'][1]
        flag=0

        for j in msg:
            topic_son=j[0]
            if 'topic' in topic_son:
                son_by_json.add(topic_son[-1])
            if 'load' in topic_son and len(topic_son[-2])>0:
                parent=topic_son[-1]
                child=topic_son[-2]
                url2='https://www.zhihu.com/topic/'+id+'/organize/entire'+'?child='+child+'&parent='+parent
                flag=1
                print url2
                logging.info(url2)

        if flag==0:
            break
        # tell me more than 5000 childs
        for num in range(1000,500,-100):
            if tmp>num:
                print id,'has more than',num*10,'child nodes'
                break

    
    print id, 'finished!'

    topic['son']=list(son_by_json) 
    html_dir = os.path.join(CUR_DIR,'DateStorage',NOW)
    html_path = os.path.join(html_dir,str(id)+'.html')

    with open(html_path,'w') as f:
        f.write(content)

    lock1.acquire()
    print>>topic_log_f, id+':=>',','.join(topic['son'])
    topic_f.write(json.dumps(topic).encode('utf8') + '\n')
    lock1.release()

    return topic['son']




class ZhihuSpider(object):
    """抓取知乎Topic的爬虫"""
    def __init__(self):
        self.dir_root = os.path.dirname(os.path.abspath(__file__))

        fname_settings = CUR_FNAME_SETTINGS
        self.configs = get_configs(fname_settings)

        self.url_homepage = self.configs['URL']['HOMEPAGE']
        self.headers_base = self.configs['HEADERS']['BASE']

        self.url_login = self.configs['URL']['LOGIN']
        self.email = self.configs['AUTH']['EMAIL']
        self.password = self.configs['AUTH']['PASSWORD']
        self.payload_login = {
            'email': self.email,
            'password': self.password,
            'rememberme': 'True',
        }

        self.url_questions = self.configs['URL']['QUESTIONS']
        self.payload_question = self.configs['PAYLOAD']['QUESTION']

        self.url_question_prefix = self.configs['URL']['QUESTION_PREFIX']

        self.timeout_query = self.configs['TIMEOUT']['QUERY']

        self.offset = self.configs['OFFSET']

        self.spider = requests.Session()
        self.spider.headers = self.headers_base

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
        with open(COOKIES) as f:
            cookies=json.loads(f.read())
            requests.utils.add_dict_to_cookiejar(self.spider.cookies, cookies)
            with open(_XSRF_GLOBAL_FIELNAME,'w') as f:
                f.write(cookies['_xsrf'])
        return self._test_login()

    def login(self):
        """登陆
        """
        if self.login_method2():
            print u'登录2',
            print 'Login successfully! '
        else:
            print 'Failed!'
            sys.exit(-1)


    
    def clean_cookies2cookies_data(self):
        """make cookies raw to a json
        """
        with open(COOKIES_RAW) as f:
            line=f.readline()
            line=line.split(';')
            cookies=dict()
            for i in line:
                index=i.find('=')
                value=i[index+1:].strip()
                value=value.replace('"','')
                cookies[i[:index].strip()]=value
            rs_f=file(COOKIES,'w')
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


    def crawl_by_layer(self):
        cur_layer=0
        id_set=set()
        cur_id_list=['19776749']

        pool=ThreadPool(6)

        topic_log_filename = NOW+'_topicSpider.log'
        topic_log_f = file(topic_log_filename,'a')

        while True:
            time.sleep(0.1)

            time1 = time.time()

            print>>topic_log_f, 'Cur_layer:'+str(cur_layer)

            next_id_list=[]
            current_dir = os.path.abspath('.')
            data_dir = os.path.join(current_dir,'DateStorage',NOW)

            if not os.path.exists(data_dir):
                os.makedirs(data_dir)

            topic_filename=os.path.join(data_dir,'layer'+str(cur_layer)+'.json')
            topic_f = file(topic_filename,'w')
            #遍历当前的id列表
            tmp = []
            for i in cur_id_list:
                if i not in id_set:
                    tmp.append((self.spider,i,topic_f,topic_log_f))
                    id_set.add(i)

            results=pool.map(multi_run_wrapper, tmp)

            print results
            for son_url_list in results:
                next_id_list.extend(son_url_list)  

            cur_id_list=list(next_id_list)

            time2 = time.time()
            print len(cur_id_list),time2-time1,'sec'

            cur_layer+=1
            if len(next_id_list)==0:break

        pool.close()
        pool.join()

        print>>topic_log_f,str(cur_layer)+' layers has been crawled!'


    def run(self):
        """总控
        """
        self.login()
        self.crawl_by_layer()


def test():
    zhihu_spider = ZhihuSpider()
    zhihu_spider.login()
    spider = zhihu_spider.spider
    id = '19776751'
    topic_f = file('19776751.txt','w')
    topic_log_f = file('19776751.log','w')
    print get_topics(spider,id,topic_f,topic_log_f)
    # with open(_XSRF_GLOBAL_FIELNAME) as f:
    #     _xsrf=f.read()
    # data_xsrf={'_xsrf':_xsrf}
    # url = 'https://www.zhihu.com/topic/19776751/organize/entire?child=19623639&parent=19776751'
    # res2=spider.post(url, data=data_xsrf,
    #                          headers=CUR_HEADERS_BASE,
    #                          timeout=CUR_TIMEOUT_QUERY)
    # data=json.loads(res2.content)
    # print json.dumps(data)

if __name__ == '__main__':
    test()
    # zhihu_spider = ZhihuSpider()
    # zhihu_spider.run()
