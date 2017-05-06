#coding=utf8


import os
import json
import random


import pandas as pd
import lxml.html as html
import MySQLdb
from multiprocessing.dummy import Pool as ThreadPool


def read_all_data():
    '''
    将所有的json数据读入
    :return: 返回所有的数据作为一个dict
    '''
    all_data = dict()
    for i in os.listdir('2017-03-18'):
        if i.find('json') != -1:
            file_p = os.path.join('2017-03-18',i)
            with open(file_p) as f:
                for line in f.readlines():
                    json_data = json.loads(line.strip())
                    _id = json_data['id']
                    if _id not in all_data:
                        all_data[_id] = json_data
                    else:
                        print u'数据重复', _id
                        
    return all_data

def discovery():
    '''
    讨论是否未归类的儿子都是一层结构
    '''
    data = dict()
    is_not_class = []
    with open('others/2017-03-18_topicSpider.log') as f:
        for i in f.readlines():
            if i.find('=>') != -1:
                line = i.split(':=>')
                parent = line[0].strip()
                son = line[1].strip().split(',')
                data[parent] = son
                if parent == '19776751':
                    is_not_class = son
        sum = 0
        print len(is_not_class) ,'nodes'
        for i in is_not_class:
            if(len(data[i]))!=1:
                print i,len(data[i])
            sum += len(data[i])
        print sum, len(is_not_class), float(sum)/len(is_not_class)



def read_items(filename):
    '''
    '''
    connection = MySQLdb.connect(host, user, password, db,charset="utf8")
    cursor = connection.cursor()
    connection.set_character_set('utf8')
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    cursor.close()
    connection.close()
    thread_list = list()
    f=file(filename)
    pool=ThreadPool(50)
    items=[]
    for line in f.readlines():
        item=json.loads(line.strip())
        # process_a_topic(item)
        items.append(item)
    pool.map(process_a_topic,items)
    pool.close()
    pool.join()

def write2mysql():
    topic_data = read_all_data()
    



def process(topic_data, cur_id, parent_id,id):
    host = '127.0.0.1'
    user = 'root'
    password = ''
    db = 'zhihu_topic'
    tmp=dict()
    connection = MySQLdb.connect(host, user, password, db,charset="utf8")
    cursor = connection.cursor()
    connection.set_character_set('utf8')
    
    topic_item = topic_data[cur_id]

    tmp['id'] = id
    tmp['t_topic_id']= cur_id
    tmp['t_topic_name']= topic_item['name'].encode('utf8')
    tmp['t_topic_parentid'] = parent_id
    tmp['t_topic_haschildren'] = len(topic_item['son'])
    tmp['t_topic_followers'] = topic_item['followers']
    des = topic_item.get('des','').encode('utf8')
    node = lxml.html.fromstring(des.decode('utf8'))
    content_xpath = '//div[@class="zm-editable-content"]/text()'
    etree2 = node.xpath(content_xpath)
    tmp['des']=','.join(etree2).encode('utf8') if len(etree2)>0 else ''

    son=topic_item['son']
    sql = 'insert into node('
    sql += ','.join(tmp.keys())+')values'
    sql+='('+','.join(['%s']*len(tmp))+')'
    cursor.execute(sql, tmp.values())
    
    cursor.close()
    connection.commit()
    connection.close()

       


if __name__ == '__main__':
    main()
