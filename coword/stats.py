#coding=utf8

import json
import jieba
import re
import lxml.html
import jieba.analyse
import codecs


import pandas as pd
from config.Config import QUESTION_DATA_DIR, ANSWER_DATA_DIR
from config.Config import STOPWORD, TOPICDICT, QUESTION_TOPIC
import MySQLdb





class Answer(object):
    """docstring for Answer"""
    
    def _get_content(self,data):
        content=''.join([i.strip() for i in data])
        try:
            etree=lxml.html.fromstring(content)
            time=etree.xpath('//text()')
        except Exception, e:
            ttt.write(content.encode('utf8')+'\n')
            return ''
        return ''.join([i.strip() for i in time])
    
    def _get_num(self,data):
        content=''.join([i.strip() for i in data])
        try:
            etree=lxml.html.fromstring(content)
            time=etree.xpath('//a')
            img=etree.xpath('//img')
        except Exception, e:
            return (0,0)
        return len(time),len(img)
    

    def __init__(self, json_data):
        super(Answer, self).__init__()
        self.time = json_data['a_time']
        self.a_agree_num = json_data["a_agree_num"]
        self.a_qid = json_data["a_qid"]
        self.a_comment_num = json_data["a_comment_num"]
        self.a_thanks_num = json_data["a_thanks_num"]
        self.user_name = json_data['a_user']

        self.content=self._get_content(json_data['a_content'])

        self.a_or_img_num=self._get_num(json_data['a_content'])

        self.dict=word_cut(self.content)
        
        
class Question(object):
    """docstring for Question"""
    def _get_the_num(self,data):
        tmp=re.search('[0-9]+',data)
        return tmp.group() if tmp else 0

    def _get_topic(self,data):
        rs=[]
        for i in data:
            etree=lxml.html.fromstring(i)
            topic_id=etree.xpath('//a/@data-token')
            topic_label=etree.xpath('//a/text()')
            tmp=dict()
            tmp['id']=topic_id
            tmp['label']=''.join([j.strip() for j in topic_label]).encode('utf8')
            rs.append(tmp)
        return rs

    def _get_the_des(self,data):
        rs=''.join(data).encode('utf8')
        return rs

    def _get_a_list(self,data):
        rs=[]
        for i in data:
            a=Answer(i)
            rs.append(a)
        return rs

    def __init__(self, content):
        json_data=json.loads(content)
        self.q_view_num = self._get_the_num(json_data['q_view_num'])
        self.q_follower_num=self._get_the_num(json_data['q_follower_num'])
        self.q_related_topic_num=self._get_the_num(json_data['q_related_topic_num'])
        self.q_url_id=self._get_the_num(json_data['q_url'])
        self.q_topic=self._get_topic(json_data['q_topic'])
        self.q_answer=self._get_the_num(json_data['q_answer_num'])
        self.q_des=self._get_the_des(json_data['q_des'])
        self.q_title=json_data['q_titile'].encode('utf8')
        self.q_answer_list=self._get_a_list(json_data['q_answer_list'])
        # f=file('lol_a1.txt','a')
        # for a in self.q_answer_list:
        #   f.write(self.q_url_id.encode('utf8')+','+a.time.encode('utf8')+','+str(len(a.content))\
        #       +','+a.comment_num.encode('utf8')+','+a.agree_num.encode('utf8')+','+str(a.a_or_img_num[0])+','+str(a.a_or_img_num[1])+'\n')

        # print self.q_url_id
        # print len(self.q_answer_list)


def read_stopword():
    '''
    读取停用词，返回一个集合
    '''
    stopword=set()
    f=codecs.open(STOPWORD,'r','utf8')
    for i in f.readlines():
        stopword.add(i.strip().encode('utf8'))
    return stopword



def word_cut(sentence):
    jieba.load_userdict(TOPICDICT)

    seg_list=jieba.cut(sentence,cut_all=False)
    tmp=[i.encode('utf8') for i in seg_list]
    # print ','.join([i for i in tmp])
    # print '-'*10
    # print ','.join([i for i in tmp if i not in stopword])
    return [i for i in tmp if i not in stopword]


def question_dict_gen():
    f = codecs.open(QUESTION_TOPIC, 'r', 'utf8')
    question_dict = set()
    for line in f.readlines():
        word_list = line.strip().split(',')
        for word in word_list:
            w1 = re.findall(u"(.*)(（.*）)",word)
            if len(w1)>0:print w1
            if word not in question_dict:
                question_dict.add(word)
    f = file(TOPICDICT,'w')
    for word in question_dict:
        f.write(word.encode('utf8')+'\n')


    

def main():
    print 'begin'
    question_dict_gen()
    # with open('19605346.json') as f:
    #     print 'begin'
    #     for i in f.readlines():
    #         content=i.strip()
    #         question=Question(content)
    #         question_answer=[x.dict for x in question.q_answer_list]
    #         all=[]
    #         for j in question_answer:
    #             all.extend(j)
    #         print len(all)
    #         with open(question.q_url_id+'.txt','w') as f:
    #             for t in all:
    #                 f.write(t+'\n')
    #         # print question.q_url_id,len(question.q_title.decode('utf8')),len(question.q_des.decode('utf8')),\
    #         # len(question.q_topic),question.q_view_num,question.q_follower_num,\
    #         # question.q_related_topic_num,question.q_answer,len(question.q_answer_list)
    #         # print [len(j.answer_term) for j in question.q_answer_list]
    print 'end'
if __name__ == '__main__':
    main()